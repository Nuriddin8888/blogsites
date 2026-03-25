from .models import Person, Blog, Comment
from django import forms
from django.contrib.auth.forms import UserCreationForm


class PersonRegister(UserCreationForm):
    class Meta:
        model = Person
        fields = ['username', 'password1', 'password2']


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['username', 'desc', 'avatar']



class BlogCreate(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'desc', 'imgage', 'sub_title', 'sub_desc', 'sub_imgage']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]