from codechallenge.models import SampleImages
import json
from django.conf import settings
from slack import WebClient


class MessageResponse:

    def __init__(self, prefix, send_only_plain_reply):
        self.prefix = prefix
        self.send_only_plain_reply = send_only_plain_reply
        self.message_attachments = [
            {
                "fallback": "label images",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "callback_id": "menu_options_2319",
                "text": "Select a Label",
                "image_url": "??",
                "actions": [
                    {
                        "name": "select_list",
                        "text": "Please select label",
                        "type": "select",
                        "options": [
                            {
                                "text": "daisy",
                                "value": "daisy"
                            },
                            {
                                "text": "dandelion",
                                "value": "dandelion"
                            },
                            {
                                "text": "rose",
                                "value": "rose"
                            },
                            {
                                "text": "sunflower",
                                "value": "sunflower"
                            },
                            {
                                "text": "sunflower",
                                "value": "sunflower"
                            }
                        ]

                    }
                ]
            }
        ]

    SUCCESS_RESPONSE = "Your input is recored sucessfully"
    FAILURE_RESPONSE = "Invalid input. Please send request in following format url:{IMAGE_URL},label:{IMAGE_LABEL}"

    def send_ask_label_question(self, client, channel, text):

        query_result = SampleImages.objects.filter(processed=0)
        if query_result != None and len(query_result) > 0:
            self.message_attachments[0]['image_url'] = query_result[0].image_url
            self.message_attachments[0]['callback_id'] = f"{self.prefix}_menuoption_{query_result[0].id}"
            jsondata = json.dumps(self.message_attachments)
            client.api_call('chat.postMessage', json={'channel': channel, 'attachments': jsondata})
            query_result[0].processed = 1
            query_result[0].save()
            return True
        else:
            return False

    def send_ask_label_question_response(self, message_text, client, channel, message_ts):
        client.api_call('chat.delete',
                        json={'channel': channel, 'text': message_text, 'ts': message_ts, 'attachments': []})
        client.api_call('chat.postMessage', json={'channel': channel, 'text': message_text})

    def send__success_question_response(self, type, client, channel, message_ts):
        return self.send__question_response(type, self.prefix + MessageResponse.SUCCESS_RESPONSE, client, channel,
                                            message_ts)

    def send__failure_question_response(self, type, client, channel, message_ts):
        return self.send__question_response(type, self.prefix + MessageResponse.FAILURE_RESPONSE, client, channel,
                                            message_ts)

    def send__question_response(self, type, message_text, client, channel, message_ts):
        if self.send_only_plain_reply:
            client.api_call('chat.postMessage', json={'channel': channel, 'text': message_text})
        elif type == 'interactive_message':
            self.send_ask_label_question_response(message_text, client, channel, message_ts)
        elif not self.send_ask_label_question(client, channel, message_text):
            client.api_call('chat.postMessage', json={'channel': channel, 'text': message_text})
