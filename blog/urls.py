from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index), 
    path('', views.PostList.as_view()), 
    # if integer -> call single_postpage
    path('<int:pk>/', views.PostDetail.as_view()),
]   