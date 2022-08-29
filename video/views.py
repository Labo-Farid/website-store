from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from video.forms import CommentForm, VideoForm
from .models import *
from marketing.forms import EmailSignupForm
from marketing.models import Signup

from store.models import *

# Create your views here.


# def search(request):
#     queryset = Video.objects.all()
#     query = request.GET.get('q')
#     if query:
#         queryset = queryset.filter(
#             Q(title__icontains=query) |
#             Q(description__icontains=query)
#         ).distinct()
#
#     most_recent = Video.objects.order_by('-timestamp')[:6]
#     recent_free_musics = Item.objects.order_by('-created')[:1]
#     context = {
#         'queryset': queryset,
#         'most_recent': most_recent,
#         'recent_free_musics': recent_free_musics,
#     }
#     return render(request, 'video/video_search_results.html', context)


def get_category_count():
    queryset = Video \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


def video_list(request, category=None):
    most_recent = Video.objects.order_by('-timestamp')[:6]
    recent_free_musics = Item.objects.order_by('-created')[:1]

    video_list = Video.objects.all()
    videos = video_list.filter(status='published')
    categories = Category.objects.all()

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    paginator = Paginator(videos, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'videos': videos,
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'recent_free_musics': recent_free_musics,
        'categories': categories,
        'page_request_var': page_request_var,
    }
    return render(request, 'video/video_home.html', context)


def video_category(request, cats):
    most_recent = Video.objects.order_by('-timestamp')[:6]
    recent_free_musics = Item.objects.order_by('-created')[:1]

    category_posts = Video.objects.filter(categories=cats)
    category_posts = category_posts.filter(status='published')

    paginator = Paginator(category_posts, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'category_posts': category_posts,
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'recent_free_musics': recent_free_musics,
        'cats': cats,
        'page_request_var': page_request_var,
        'form': form
    }
    return render(request, 'video/video_category.html', context)


def video_detail(request, slug):
    most_recent = Video.objects.order_by('-timestamp')[:3]
    video = get_object_or_404(Video, slug=slug)

    if request.user.is_authenticated:
        VideoView.objects.get_or_create(user=request.user, video=video)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = video
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': video.pk
            }))

    context = {
        'video': video,
        'most_recent': most_recent,
        'form': form
    }
    return render(request, 'video/video_detail.html', context)


