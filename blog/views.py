from django.shortcuts import render
from django.views.generic import ListView, DeleteView
from .models import Post

# Create your views here.

# Class Based View

class PostList(ListView) :
    model = Post
    template_name = 'blog/post_list.html'

class PostDetail(DeleteView) :
    model = Post

'''
# Function Based View

def index(request) : 
    # Get Query
    posts = Post.objects.all()

    return render (
        request,
        'blog/index.html',
        {
            'posts': posts,
        }
    )

def single_post_page(request, pk) :
    post = Post.objects.get(pk=pk)

    return render (
        request, 
        'blog/single_post_page.html', 
        {
            'post': post, 
        }
    )
'''