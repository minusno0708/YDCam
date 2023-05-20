import time
import datetime

from django.core.files.base import ContentFile
from .models import Record

def record_capture(image):
    now = datetime.datetime.now()
    image_name = str(time.mktime(now.timetuple()) * 1000) + "jpg"
    record_image = Record()
    record_image.image.save(image_name,ContentFile(image))
    record_image.save()  