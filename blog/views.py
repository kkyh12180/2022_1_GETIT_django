from django.shortcuts import render
from .models import Post

# Create your views here.

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