from django import forms
from .models import Post, Profile, Blog, Comment


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "bio", "website"]
        widgets = {
            "bio": forms.Textarea(attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none",
                "rows": 3,
                "placeholder": "Write something about yourself..."
            }),
            "website": forms.URLInput(attrs={
                "class": "w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-400 focus:outline-none",
                "placeholder": "https://yourwebsite.com"
            }),
            "avatar": forms.ClearableFileInput(attrs={
                "class": "hidden"
            }),
        }
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

# Form for Blog model
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  