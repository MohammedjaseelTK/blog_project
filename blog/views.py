from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from .models import Post, Profile, Comment, Follow, Category
from .forms import PostForm, ProfileForm, CommentForm, BlogForm


def index(request):
    posts = Post.objects.all().order_by('-created_at')  # latest 3 only
    return render(request, 'blog/index.html', {'posts': posts})

def home(request):
    posts = Post.objects.all().order_by('-created_at')  # full feed
    return render(request, 'blog/home.html', {'posts': posts})


def blog_feed(request):  # this will be the NEW blog feed
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/feed.html', {'posts': posts})


def latest_posts(request):
    posts = Post.objects.select_related('author').order_by('-created_at')[:8]
    return render(request, 'blog/latest_blogs.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    user_liked = request.user.is_authenticated and request.user in post.likes.all()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'user_liked': user_liked,
    })

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            messages.success(request, 'Post created!')
            return redirect('post_detail', post_id=obj.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form, 'mode': 'Create'})

@login_required
def edit_post(request, post_id=None, pk=None):
    post_pk = post_id if post_id is not None else pk
    post = get_object_or_404(Post, pk=post_pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated!')
            return redirect('post_detail', post_id=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {'form': form, 'mode': 'Edit'})

@login_required
def delete_post(request, post_id=None, pk=None):
    post_pk = post_id if post_id is not None else pk
    post = get_object_or_404(Post, pk=post_pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('index')
    return render(request, 'blog/confirm_delete.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)  # reuse BlogForm for simple auth or switch to UserCreationForm
        # This is placeholder; recommend using UserCreationForm in real project
        return redirect('index')
    else:
        form = BlogForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    from django.contrib.auth.forms import AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


def logout_view(request):
    logout(request)   # logs out user
    return redirect('login')  #
    
@login_required
def profile_view(request, username):
    user_obj = get_object_or_404(User.objects.select_related('profile'), username=username)
    
    # Get posts authored by this user
    posts = Post.objects.filter(author=user_obj)

    # Check if the logged-in user follows this profile user
    is_following = Follow.objects.filter(follower=request.user, following=user_obj).exists()

    # Count followers and following using your Follow model
    followers_count = Follow.objects.filter(following=user_obj).count()
    following_count = Follow.objects.filter(follower=user_obj).count()

    context = {
        'user_obj': user_obj,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request, username):
    user_obj = get_object_or_404(User, username=username)

    # Redirect if the user tries to edit someone else's profile
    if user_obj != request.user:
        return redirect('profile', username=username)

    # Get or create the profile for this user
    profile, _ = Profile.objects.get_or_create(user=user_obj)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', username=username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'blog/edit_profile.html', {'form': form, 'user_obj': user_obj})

@login_required
def follow_unfollow(request, username):
    target_user = get_object_or_404(User, username=username)
    
    if request.user == target_user:
        return redirect('profile', username=username)  # Prevent self-follow

    follow_instance = Follow.objects.filter(follower=request.user, following=target_user)

    if follow_instance.exists():
        follow_instance.delete()
    else:
        Follow.objects.create(follower=request.user, following=target_user)

    return redirect('profile', username=username)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'like_count': post.likes.count()})
    return redirect('home')


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            if request.is_ajax():
                return JsonResponse({
                    'username': comment.user.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime("%b %d, %Y %H:%M")
                })
    return redirect('home')

def manage_categories(request):
    if request.method == "POST":
        category_name = request.POST.get("category_name")
        if category_name:
            Category.objects.create(name=category_name)
            return redirect("manage_categories")  # reload page

    categories = Category.objects.all()
    return render(request, "blog/manage_categories.html", {"categories": categories})


def about(request):
    return render(request, "blog/about.html")

def categories(request):
    return render(request, "blog/categories.html")


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)

    followers = Follow.objects.filter(following=user).count()
    following = Follow.objects.filter(follower=user).count()
    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    return render(request, 'blog/user_profile.html', {
        'profile_user': user,
        'posts': posts,
        'followers': followers,
        'following': following,
        'is_following': is_following,
    })


def all_blogs(request):
    blogs = Post.objects.all().order_by('-created_at')  # fetch all posts
    return render(request, 'adminpanel/all_blogs.html', {'blogs': blogs})