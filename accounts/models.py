from django.db import models
from django.conf import settings
# Create your models here.

class Resume(models.Model):
    POSITION_CHOICES = (
        ("개발자", '개발자'),
        ("기획자", '기획자'),
        ("디자이너", "디자이너"),
    )
    GROUP_CHOICES = (
        ("피로그래밍","피로그래밍"),
        ("SNUSV","SNUSV"),
        ("창업맞춤형사업", "창업맞춤형사업"),
        ('SNULitez', 'SNULitez'),
        ('해동 아이디어팩토리', '해동 아이디어팩토리'),
        ("기타","기타"),
    )
    SIZE_CHOICES = (
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL"),
        ("XXL","XXL"),
        ("XXXL","XXXL"),
    )
    name = models.CharField(max_length=100)
    contents = models.TextField(max_length=500)
    group = models.CharField(max_length=20, choices=GROUP_CHOICES)
    position = models.CharField(max_length=20, choices = POSITION_CHOICES)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete =models.CASCADE)
    t_size = models.CharField(max_length=10, choices=SIZE_CHOICES, default="L")
