from django.urls import path, include

from video.views import *

urlpatterns = [
    path('', video_list, name='video_home'),
    path('video/<str:slug>/', video_detail, name='video_detail'),
    path('category/<str:cats>/', video_category, name='video_category_list'),
    # path('search/', search, name='search'),
]

