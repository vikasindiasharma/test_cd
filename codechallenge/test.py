from django.test import TestCase
from codechallenge.message_handler import MessageHandler
from codechallenge.message_handler import RESPONSE_PREFIX
from codechallenge.message_parser import MessageParser

class MessageHandlerTestCase(TestCase):
#    def setUp(self):
        #Animal.objects.create(name="lion", sound="roar")
        #Animal.objects.create(name="cat", sound="meow")

    def test_App_generated_message_are_ignored(self):
        handler= MessageHandler()
        result=handler.can_ignore_message( RESPONSE_PREFIX + "  test")
        self.assertEqual(result, True)

    def test_blank_message_are_ignored(self):
        handler= MessageHandler()
        result=handler.can_ignore_message( None)
        self.assertEqual(result, True)


    def test_non_app_message_are_not_ignored(self):
        handler= MessageHandler()
        result=handler.can_ignore_message( "url:http://rose.png,label:test")
        self.assertEqual(result, False)

class MessageParserTestCase(TestCase):

    def test_valid_message_pass_validation(self):
        parser= MessageParser()
        result=parser.parse( "url:http://rose.png,label:daisy")
        self.assertEqual(result, True)
        self.assertEqual(parser.is_valid_message, True)

    def test_message_without_url_not_valid(self):
        parser= MessageParser()
        result=parser.parse( "label:daisy")
        self.assertEqual(result, False)
        self.assertEqual(parser.is_valid_message, False)

    def test_message_without_label_not_valid(self):
        parser= MessageParser()
        result=parser.parse( "url:http:\\test.png")
        self.assertEqual(result, False)
        self.assertEqual(parser.is_valid_message, False)

    def test_message_with_invalid_label_value_not_valid(self):
        parser= MessageParser()
        result=parser.parse( "label:test:url:http:\\test.png")
        self.assertEqual(result, False)
        self.assertEqual(parser.is_valid_message, False)