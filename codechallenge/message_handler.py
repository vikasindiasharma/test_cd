from codechallenge.models import ImageLabel
from codechallenge.message_parser import MessageParser
from django.utils import timezone
from codechallenge.message_response import MessageResponse


def send_response(response) -> str:
    return RESPONSE_PREFIX + response

RESPONSE_PREFIX: str = "@@App "

class MessageHandler:

    def can_ignore_message(self, message):
        if message and  not message.startswith(RESPONSE_PREFIX) :
            self.ignore_message = False
        else:
            self.ignore_message = True

        return self.ignore_message


    def process_message(self, message,atttachments):

        # As of now support is of only one attachment. If attachment is provided then text message will be ignored
        if atttachments != None and len(atttachments) ==1 and type(atttachments[0] is dict):
                url = atttachments[0].get("image_url")
                label= atttachments[0].get("text")
                message=f"url:{url},label:{label}"

        if self.can_ignore_message(message):
            return None

        parser = MessageParser()

        if parser.parse(message):

            query_result = ImageLabel.objects.filter(image_url=parser.image_url)
            if len(query_result)== 1:
                image_label  =query_result[0]
                image_label.image_label=parser.image_label

            else:
                image_label = ImageLabel(image_url=parser.image_url, image_label=parser.image_label,
                                     createdDate=timezone.now())

            print(image_label)
            image_label.save()
            return send_response(MessageResponse.SUCCESS_RESPONSE)
        else:
            return send_response(MessageResponse.FAILURE_RESPONSE)


#handler = MessageHandler()
#print(handler.process_message("label:ABC,url:https://hh.comh,"))
