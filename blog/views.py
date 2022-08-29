from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CommentForm, PostForm
from .models import Post, Author, PostView
from marketing.forms import EmailSignupForm
from marketing.models import Signup

from store.models import *

form = EmailSignupForm()


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


# class SearchView(View):
#     def get(self, request, *args, **kwargs):
#         queryset = Post.objects.all()
#         query = request.GET.get('q')
#         if query:
#             queryset = queryset.filter(
#                 Q(title__icontains=query) |
#                 Q(overview__icontains=query)
#             ).distinct()
#         context = {
#             'queryset': queryset
#         }
#         return render(request, 'blog/search_results.html', context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    most_recent = Post.objects.order_by('-timestamp')[:6]
    recent_free_musics = Item.objects.order_by('-created')[:1]
    context = {
        'queryset': queryset,
        'most_recent': most_recent,
        'recent_free_musics': recent_free_musics,
    }
    return render(request, 'blog/search_results.html', context)


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


# class IndexView(View):
#     form = EmailSignupForm()
#
#     def get(self, request, *args, **kwargs):
#         featured = Post.objects.filter(featured=True)
#         latest = Post.objects.order_by('-timestamp')[0:3]
#         context = {
#             'object_list': featured,
#             'latest': latest,
#             'form': self.form
#         }
#         return render(request, 'blog/index.html', context)
#
#     def post(self, request, *args, **kwargs):
#         email = request.POST.get("email")
#         new_signup = Signup()
#         new_signup.email = email
#         new_signup.save()
#         messages.info(request, "Successfully subscribed")
#         return redirect("blog_home")


def index(request):
    most_recent = Post.objects.order_by('-timestamp')[:6]
    recent_musics = Item.objects.order_by('-created')[:6]

    post_list = Post.objects.all()
    posts = post_list.filter(status='published').order_by('-timestamp')[:4]
    categories = Category.objects.all()

    item_list = Item.objects.all()
    items = item_list.filter(status='published')

    form = EmailSignupForm()
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")

    context = {
        'posts': posts,
        'items': items,
        'most_recent': most_recent,
        'recent_musics': recent_musics,
        'categories': categories,
        'object_list': featured,
        'latest': latest,
        'form': form
    }

    return render(request, 'blog/index.html', context)


# class PostListView(ListView):
#     form = EmailSignupForm()
#     model = Post
#     template_name = 'blog/blog.html'
#     context_object_name = 'queryset'
#     paginate_by = 10
#
#     def get_context_data(self, **kwargs):
#         category_count = get_category_count()
#         most_recent = Post.objects.order_by('-timestamp')[:6]
#         recent_free_musics = Item.objects.order_by('-created')[:1]
#         context = super().get_context_data(**kwargs)
#         context['most_recent'] = most_recent
#         context['recent_free_musics'] = recent_free_musics
#         context['page_request_var'] = "page"
#         context['category_count'] = category_count
#         context['form'] = self.form
#         return context


def post_list(request, category=None):
    most_recent = Post.objects.order_by('-timestamp')[:6]
    recent_musics = Item.objects.order_by('-created')[:6]

    post_list = Post.objects.all()
    posts = post_list.filter(status='published')
    categories = Category.objects.all()

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    paginator = Paginator(posts, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'recent_musics': recent_musics,
        'categories': categories,
        'page_request_var': page_request_var,
        'form': form
    }
    return render(request, 'blog/blog.html', context)


def post_category(request, cats):
    most_recent = Post.objects.order_by('-timestamp')[:6]
    recent_musics = Item.objects.order_by('-created')[:6]

    category_posts = Post.objects.filter(categories=cats)
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
        'recent_musics': recent_musics,
        'cats': cats,
        'page_request_var': page_request_var,
        'form': form
    }
    return render(request, 'blog/post_category.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        # post = get_object_or_404(Post, slug=self.kwargs.get('slug'))
        most_recent = Post.objects.order_by('-timestamp')[:6]
        recent_musics = Item.objects.order_by('-created')[:6]
        # related_posts = Post.objects.filter(categories=post.categories).order_by('-created').exclude(id=post.id)[:9]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['recent_musics'] = recent_musics
        # context['related_posts'] = related_posts
        context['page_request_var'] = "page"
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            }))


def post_detail(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    recent_musics = Item.objects.order_by('-created')[:6]
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'post': post,
        'most_recent': most_recent,
        'recent_musics': recent_musics,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'blog/post.html', context)


class PostCreateView(CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog/post_create.html", context)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "blog/post_create.html", context)


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'blog/post_confirm_delete.html'


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))
