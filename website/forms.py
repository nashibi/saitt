from django import forms
from website.models import Category, Post


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'