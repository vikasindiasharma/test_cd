from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack import WebClient
from codechallenge.message_handler import MessageHandler
from codechallenge.sample_images import sample_data


import json
from django.views.decorators.http import require_http_methods

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
Client = WebClient(SLACK_BOT_USER_TOKEN)

class HandleSlackEvents(APIView):

    def __init__(self):
        self.counter=1

    def post(self, request, *args, **kwargs):

        print(f"countre.... {sample_data[0]}")


        slack_message = request.data
        print(slack_message)
        try:
            form_json =  json.loads(slack_message.get('payload'))
            print(type(form_json))
          #  print(f"*************** type : {form_json.get('actions')[0].get('selected_options')[0].get('value')} ************************    ")
            print(f"*************** attachments : {form_json.get('original_message').get('attachments')[0].get('image_url')} ************************    ")
            print(f"*************** attachments : {form_json.get('original_message').get('attachments')[0].get('imageIndex')} ************************    ")
        except:
            print("Error")
        if slack_message.get('token') != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # verification challenge
        if slack_message.get('type') == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)
        # greet bot
        if 'event' in slack_message:
            message_attachments = [
                {
                    "fallback": "label images",
                    "color": "#3AA3E3",
                    "attachment_type": "default",
                    "callback_id": "menu_options_2319",
                    "text": "Select a Label",
                    'imageIndex':'0',
                    "image_url": "https://images.wagwalkingweb.com/media/articles/cat/daisy-poisoning-1/daisy-poisoning-1.jpg",
                    "actions": [
                        {
                            "name": "games_list",
                            "text": "Pick a game...",
                            "type": "select",
                            "options": [
                                {
                                    "text": "Chess",
                                    "value": "chess"
                                },
                                {
                                    "text": "Global Thermonuclear War",
                                    "value": "war"
                                }
                            ]

                        }
                    ]
                }
            ]

            message_handler = MessageHandler()
            event_message = slack_message.get('event')
            text = event_message.get('text')
            attachments = event_message.get('attachments')
            response = message_handler.process_message(text, attachments)
            channel = event_message.get('channel')
            jsondata = json.dumps(message_attachments)
            if text == "hi":
                Client.api_call('chat.postMessage', json={'channel': channel, 'attachments': jsondata})
            # if not message_handler.ignore_message:
            # Client.api_call('chat.postMessage', json={'channel': channel, 'text': response})
        #           Client.api_call('chat.postMessage', json={'channel': channel, 'attachments':jsondata})
        # else:
        #   print("Message ignored !!")
        return Response(status=status.HTTP_200_OK)