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