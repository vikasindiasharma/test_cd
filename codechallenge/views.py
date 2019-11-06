from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from slack import WebClient
from codechallenge.message_handler import MessageHandler
from codechallenge.csv_loader import load_csv

import json
from django.views.decorators.http import require_http_methods

SLACK_VERIFICATION_TOKEN = getattr(settings, 'SLACK_VERIFICATION_TOKEN', None)
SLACK_BOT_USER_TOKEN = getattr(settings, 'SLACK_BOT_USER_TOKEN', None)
Client = WebClient(SLACK_BOT_USER_TOKEN)


class HandleSlackEvents(APIView):

    def __init__(self):
        self.counter = 1

    def post(self, request, *args, **kwargs):

        slack_message = request.data
        print(f"**** Message Received :  {slack_message}  ******")
        payload = slack_message.get('payload')
        payload_message = False
        token = slack_message.get('token')
        type = slack_message.get('type')
        message_ts = slack_message.get('message_ts')
        channel = None
        if payload != None:
            slack_message = json.loads(payload)
            payload_message = True
            try:
                selected_value = slack_message.get('actions')[0].get('selected_options')[0].get('value')
                image_url = slack_message.get('original_message').get('attachments')[0].get('image_url')
                token = slack_message.get('token')
                type = slack_message.get('type')
                channel = slack_message.get('channel').get('id')
                message_ts = slack_message.get('message_ts')
            except:
                return Response(data='Invalid payload', status=status.HTTP_200_OK)

        if token != SLACK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        # verification challenge
        if type == 'url_verification':
            return Response(data=slack_message, status=status.HTTP_200_OK)

        message_handler = MessageHandler()
        if payload_message and type == 'interactive_message':
            # Build the url in required format
            text = f'url:{image_url},label:{selected_value}'
            message_handler.process_message(text, None, Client, channel, type, message_ts)
        elif 'event' in slack_message:
            event_message = slack_message.get('event')
            text = event_message.get('text')
            attachments = event_message.get('attachments')
            channel = event_message.get('channel')
            message_handler.process_message(text, attachments, Client, channel, type, message_ts)

        return Response(status=status.HTTP_200_OK)