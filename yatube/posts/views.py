from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Group, Post, User
from .forms import PostForm


# Следуем DRY
def paginate(request, post_list, posts_per_page=10):
    paginator = Paginator(post_list, posts_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    template = 'posts/index.html'
    post_list = Post.objects.all()
    page_obj = paginate(request, post_list)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = paginate(request, post_list)
    context = {
        'group': group,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    posts_count = post_list.count()
    page_obj = paginate(request, post_list)
    context = {
        'author': author,
        'page_obj': page_obj,
        'posts_count': posts_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    posts_count = author.posts.count()
    context = {
        'author': author,
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            post_obj = Post()
            post_obj.author = request.user
            post_obj.text = form.cleaned_data['text']
            post_obj.group = form.cleaned_data['group']
            post_obj.save()
            return redirect('posts:profile', request.user.username)

    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)

    # Пользователь может редактировать только свои посты
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)

    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        post.text = form.cleaned_data['text']
        post.group = form.cleaned_data['group']
        post.save()
        return redirect('posts:post_detail', post_id)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, template, context)
