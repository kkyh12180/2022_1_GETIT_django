from django.contrib import admin
from .models import Post, Category

'''
Admin 페이지에 무엇을 쓸지 등록
'''

# Register your models here.
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin) : 
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)