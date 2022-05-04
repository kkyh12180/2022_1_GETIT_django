from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Post(models.Model) : 
    title = models.CharField(max_length = 30)
    content = models.TextField()

    # Save Image
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    
    # 표준시 기준 -> 서울 기준 필요, 이는 settings.py를 통한 조정
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    # pk : 기본키
    def __str__(self) :
        return f'[{self.pk}] {self.title}'