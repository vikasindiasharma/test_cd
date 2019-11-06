from codechallenge.models import ImageLabel
from codechallenge.message_parser import MessageParser
from django.utils import timezone
from codechallenge.message_response import MessageResponse


def send_response(response) -> str:
    return RESPONSE_PREFIX + response


RESPONSE_PREFIX: str = "@@App "


class MessageHandler:

    def can_ignore_message(self, message):
        if message and not message.startswith(RESPONSE_PREFIX):
            self.ignore_message = False
        else:
            self.ignore_message = True

        return self.ignore_message

    def process_message(self, message, atttachments, client, channel, type, message_ts):

        send_only_plain_reply = False
        # As of now support is of only one attachment. If attachment is provided then text message will be ignored
        if atttachments != None and len(atttachments) == 1:
            url = atttachments[0].get("image_url")
            label = atttachments[0].get("text")
            message = f"url:{url},label:{label}"
            callback_id = atttachments[0].get("callback_id")
            send_only_plain_reply = True
            if callback_id != None and self.can_ignore_message(callback_id):
                return False

        if self.can_ignore_message(message):
            return False

        response = MessageResponse(RESPONSE_PREFIX, send_only_plain_reply)
        parser = MessageParser()
        if parser.parse(message):
            query_result = ImageLabel.objects.filter(image_url=parser.image_url)
            if len(query_result) == 1:
                image_label = query_result[0]
                image_label.image_label = parser.image_label

            else:
                image_label = ImageLabel(image_url=parser.image_url, image_label=parser.image_label,
                                         createdDate=timezone.now())

            image_label.save()
            return response.send__success_question_response(type, client, channel, message_ts)
        else:
            return response.send__failure_question_response(type, client, channel, message_ts)

# handler = MessageHandler()
# print(handler.process_message("label:ABC,url:https://hh.comh,"))
