from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="index"),
    path('contact', views.search_page, name="contact"),
    path('/recommend', views.BookRecommender, name='result'),

]