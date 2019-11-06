import pandas as pd
from codechallenge.models import SampleImages
from django.conf import settings
from django.db import connection

CSV_FILE_PATH = getattr(settings, 'CSV_FILE_PATH', None)



def load_csv():
    all_tables = connection.introspection.table_names()
    if "codechallenge_sampleimages" in all_tables:
        #SampleImages.objects.all().delete()
        dbRecordCount = SampleImages.objects.all().count()
        # One time upload
        if dbRecordCount == 0:
            print("One time load data..")
            sample_data = pd.read_csv(CSV_FILE_PATH)

            # with transaction.commit_on_success():
            for index in sample_data.index:
                data = sample_data['data'][index]
                image = SampleImages(image_url=data)
                image.save()
                # SampleImages.objects.create(image_url=data,processed=0 )

            dbRecordCount = SampleImages.objects.all().count()
            print(f"Total  {dbRecordCount} records imported.")


load_csv()
