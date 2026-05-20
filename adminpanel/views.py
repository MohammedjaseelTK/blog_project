# adminpanel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from blog.models import Blog, Post, Comment
from blog.forms import BlogForm
from django.views.decorators.http import require_POST

def dashboard(request):
    
    total_blogs = Blog.objects.count()
    total_likes = Post.objects.count()
    total_comments = Comment.objects.count()
    total_users = User.objects.count()

    context = {
        'total_blogs': total_blogs,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_users': total_users,
    }
    return render(request, 'adminpanel/dashboard.html', context)

def blog_list(request):
    blogs = Blog.objects.all().order_by('-id')
    return render(request, 'adminpanel/blog_list.html', {'blogs': blogs})

def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('admin_blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'adminpanel/edit_blog.html', {'form': form})

@require_POST
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    return redirect('admin_blogs')

def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'adminpanel/user_list.html', {'users': users})

def admin_likes(request):
    return render(request, 'adminpanel/admin_likes.html')

def admin_comments(request):
    return render(request, 'adminpanel/admin_comments.html')

def delete_like(request, like_id):
    like = get_object_or_404(Like, id=like_id)
    like.delete()
    return redirect("admin_likes")

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect("admin_comments")


def admin_users(request):
    users = User.objects.all()
    return render(request, "adminpanel/admin_users.html", {"users": users})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect("admin_users")

