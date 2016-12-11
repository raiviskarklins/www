from django.contrib.auth.models import User
from django import forms
from .models import Profile, Blog, Comment

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password']


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category', 'picture']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


