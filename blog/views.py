from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Category, Post, Tag

# Create your views here.

# Class Based View

class PostList(ListView) :
    model = Post
    ordering = '-pk'

    def get_context_data(self, **kwargs) :
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category = None).count()
        return context

class PostDetail(DetailView) :
    model = Post

    def get_context_data(self, **kwargs) :
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category = None).count()
        return context

def category_page(request, slug) :
    if slug == 'no_category' :
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else :
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render (
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'categories' : Category.objects.all(), 
            'no_category_post_count' : Post.objects.filter(category=None).count(), 
            'category' : category,
            
        }
    )

def tag_page(request, slug) :
    tag = Tag.objects.get(slug=slug)
    post_list = Post.objects.filter(category=None)

    return render (
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'tag' : tag, 
            'categories' : Category.objects.all(), 
            'no_category_post_count' : Post.objects.filter(category=None).count(), 
        }
    )


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