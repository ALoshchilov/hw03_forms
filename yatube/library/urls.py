from django.urls import path
from django import views

urlpatterns = [
    path('new_book/', views.BookView.as_view(), name='new_book')
]
