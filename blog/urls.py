from django.urls import path, include

from blog.views import *

from marketing.views import email_list_signup

urlpatterns = [
    # path('', IndexView.as_view(), name='blog_home'),
    path('', post_list, name='blog_home'),
    path('category/<str:cats>/', post_category, name='post_category_list'),
    # path('', PostListView.as_view(), name='blog_home'),
    path('search/', search, name='search'),
    # path('create/', post_create, name='post-create'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    # path('post/<id>/', post_detail, name='post-detail'),
    path('post/<slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<id>/update/', post_update, name='post-update'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<id>/delete/', post_delete, name='post-delete'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('email-signup/', email_list_signup, name='email-list-signup'),
]

