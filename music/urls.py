from django.urls import path
from .views import *

urlpatterns = [
    path('all-music/', GetAllMusic.as_view(),name='all_music'),
    path('music-by-singer/', GetSingerMusic.as_view(),name='all_music'),
]