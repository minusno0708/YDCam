import time
import datetime

from django.core.files.base import ContentFile
from .models import Record

def record_capture(image):
    dt_now = datetime.datetime.now()
    now = dt_now.strftime("%Y-%m-%d _%H-%M-%S")
    now += "-" + str(int(1360287003083988472 % 1000000000)).zfill(4)
    image_name = now + ".jpg"
    record_image = Record()
    record_image.image.save(image_name,ContentFile(image))
    record_image.save()  