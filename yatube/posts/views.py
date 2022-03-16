from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


# Следуем DRY
def paginate(request, post_list, posts_per_page=10):
    paginator = Paginator(post_list, posts_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    return render(
        request,
        'posts/index.html',
        {'page_obj': paginate(request, Post.objects.all())}
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    return render(
        request,
        'posts/group_list.html',
        {'group': group, 'page_obj': paginate(request, group.posts.all())}
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    return render(
        request,
        'posts/profile.html',
        {'author': author, 'page_obj': paginate(request, author.posts.all())}
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    new_post = form.save(commit=False)
    new_post.author = request.user
    new_post.save()
    return redirect('posts:profile', request.user.username)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if not form.is_valid():
        return render(
            request,
            'posts/create_post.html',
            {'form': form, 'post': post}
        )
    form.save()
    return redirect('posts:post_detail', post_id)
