from django.db import models


class ImageLabel(models.Model):
    image_url = models.CharField(max_length=5000, unique=True)
    image_label = models.CharField(max_length=9)
    createdDate = models.DateTimeField('Created Date')
    def __str__(self):
        return  f"{self.image_url},{self.image_label},{self.createdDate}"

class SampleImages(models.Model):
    image_url=models.CharField(max_length=5000)