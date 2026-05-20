from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('home/', views.home, name='Home'),
    path('feed/', views.blog_feed, name='blog_feed'), 
    path('latest/', views.latest_posts, name='latest_posts'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/', views.post_detail, name='post_detail_pk'),
    path('post/new/', views.add_post, name='add_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/', views.logout_view, name='logout'),
   
    path('<str:username>/follow/', views.follow_unfollow, name='follow_unfollow'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),
    path("about/", views.about, name="about"),
    path("categories/", views.categories, name="categories"),
    
    path('all-blogs/', views.all_blogs, name='all_blogs'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),


]