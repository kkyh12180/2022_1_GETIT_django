from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index), 
    path('create_post/', views.PostCreate.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('tag/<str:slug>/', views.tag_page),
    path('', views.PostList.as_view()), 
    # if integer -> call single_postpage
    path('<int:pk>/', views.PostDetail.as_view()),
]   