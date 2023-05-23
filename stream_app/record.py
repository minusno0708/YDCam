import datetime

from django.core.files.base import ContentFile
from .models import Record

def record_capture(conf, image):
    dt_now = datetime.datetime.now()
    now = dt_now.strftime("%Y-%m-%d _%H-%M-%S-%f")[:-4]
    image_name = now + ".jpg"
    record_image = Record()
    record_image.conf = conf
    record_image.image.save(image_name,ContentFile(image))
    record_image.save()  