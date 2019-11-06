import re


class MessageParser:
    VALLID_LABELS = ['daisy', 'dandelion', 'rose', 'sunflower', 'tulip']

    def parse(self, message):

        self.is_valid_message: bool = False
        self.image_label_found: bool = False
        self.image_url_found: bool = False
        self.image_label: str = None
        self.image_url: str = None

        temp_message = message.lower()
        result = re.findall("url:\s*([^,]+)", temp_message)
        if len(result) == 1:
            self.image_url_found = True
            self.image_url = result[0]

        result = re.findall("label:\s*([^,]+)", temp_message)
        if len(result) == 1 and result[0]  in MessageParser.VALLID_LABELS:
            self.image_label_found = True
            self.image_label = result[0]

        if self.image_label_found and self.image_url_found:
            self.is_valid_message = True

        return self.is_valid_message
