from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), 
    # if integer -> call single_postpage
    path('<int:pk>/', views.single_post_page),
]   