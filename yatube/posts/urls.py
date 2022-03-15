from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [    
    path('group/<slug:slug>/', views.group_posts, name='group_list'),

    # Профайл пользователя
    path('profile/<str:username>/', views.profile, name='profile'),

    # Работа с постами
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),   
    path('index/', views.index, name='index'), 
    path('', views.index, name='index'), 
]