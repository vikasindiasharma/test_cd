import pandas as pd
from codechallenge.models import SampleImages
print('Loading file....')

sample_data = pd.read_csv('C:\\GitGub\\final\\colabelsite\\codechallenge\\flowers.csv')

SampleImages.objects.all().delete()

for index in sample_data.head(2).index:
    data=sample_data['data'][index]
    try:
        image =SampleImages( image_url=data)
        image.save()
    except:
        print('Error' + data)

print(SampleImages.objects.all())