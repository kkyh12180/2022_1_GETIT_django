from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
class Post(models.Model) : 
    title = models.CharField(max_length = 30)
    hook_text = models.CharField(max_length = 100, blank=True)
    content = models.TextField()

    # Save Image
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)

    # 표준시 기준 -> 서울 기준 필요, 이는 settings.py를 통한 조정
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    # Author
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # pk : 기본키
    def __str__(self) :
        return f'[{self.pk}] {self.title}::{self.author}'

    def get_absolute_url(self) :
        return f'/blog/{self.pk}/'

    def get_file_name(self) : 
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self) : 
        return self.get_file_name().split('.')[-1]