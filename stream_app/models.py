from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# 画像を保存するデータモデル
class Record(models.Model):
    device = models.IntegerField(default=0)
    image = models.ImageField(upload_to='image/')
    conf = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now_add=True)
