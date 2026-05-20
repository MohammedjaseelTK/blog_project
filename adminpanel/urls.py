from django.urls import path
from . views import *

urlpatterns = [
    
    path('', dashboard, name='admin_dashboard'),
    path('blogs/', blog_list, name='admin_blogs'),
    path('blogs/edit/<int:blog_id>/', edit_blog, name='edit_blog'),
    path('blogs/delete/<int:blog_id>/',delete_blog, name='delete_blog'),
    path('users/', user_list, name='admin_users'),
    path('users/delete/<int:user_id>/', delete_user, name='delete_user'),
    
    path('likes/', admin_likes, name='admin_likes'),
    path('comments/', admin_comments, name='admin_comments'),
    path('custom-admin/likes/delete/<int:like_id>/', delete_like, name='delete_like'),
    path('custom-admin/comments/delete/<int:comment_id>/', delete_comment, name='delete_comment'),


]

