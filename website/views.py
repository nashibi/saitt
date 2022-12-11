from django.db.models import Q
from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from website.models import Post, Category
from website.serializerz import PostSerializer
from website.forms import CategoryForm, PostForm
from django.contrib import messages

from django.core.files.storage import FileSystemStorage


def home_view(request):
    context = {}
    cat_form = CategoryForm()
    post_form = PostForm()
    context['cat_form'] = cat_form
    context['post_form'] = post_form
    if request.method == 'GET':
        pass
    else:
        try:
            cat_form = CategoryForm(request.POST)
            if cat_form.is_valid():
                cat_form.save()
                messages.add_message(request, messages.SUCCESS, 'your category submitted successfully')
            else:
                messages.add_message(request, messages.ERROR, 'category submission has been failed')
        except:
            pass

        try:
            category = request.POST['category']
            if category == '':
                category = 'None'
        except:
            category = 'None'
        print('category' + category)
        try:
            title = request.POST['title']
            content = request.POST['content']
            try:
                reply_to = request.POST['reply_to']
            except:
                reply_to = None

            try:
                img = request.FILES['img']
                fss = FileSystemStorage()
                fss.save(img.name, img)
            except:
                img = None
                print('none')
            try:
                print(request.POST['category'])
                cat = Category.objects.get(name__exact=category)
            except:
                cat = Post.objects.get(title=str(reply_to)).category
            try:
                reply_to = Post.objects.get(title=str(reply_to))
            except:
                reply_to = None
            print('title: ' + str(title))
            print('author: ' + str(request.user))
            print('category: ' + str(cat))
            print('content: ' + str(content))
            print('reply_to: ' + str(reply_to))

            new_post = Post(
                title=request.POST['title'],
                author=request.user,
                image=img,
                content=request.POST['content'],
                reply_to=reply_to,
            )
            new_post.save()
            new_post.category.add(cat)
            new_post.save()

        except Exception as e:
            print(str(e))
            pass
    categories = Category.objects.all()
    context['categories'] = categories
    posts = Post.objects.all().order_by('id')
    context['posts'] = posts
    return render(request, 'home.html', context)


class Paginator(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000


class post_related_ajax(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    pagination_class = Paginator

    def get_queryset(self):
        post_title = self.request.POST['post_data']
        print(1)
        print(post_title)
        post = Post.objects.get(title=str(post_title))
        posts = Post.objects.filter(reply_to=post)
        print("posts: " + str(posts))
        return posts

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_paginated_response(self, data):
        return Response(data)


class ajax_cat_post(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = PostSerializer
    pagination_class = Paginator

    def get_queryset(self):
        try:
            category = self.request.POST['category']
            if category == "":
                category = 'None'
        except:
            category = 'None'
        if category != 'None':
            if category == 'همه دسته ها':
                posts = Post.objects.filter()
                print("posts: " + str(posts))
                return posts
            else:
                category = Category.objects.get(name=category)
                posts = Post.objects.filter(category__name__exact=category.name)
                print("posts: " + str(posts))
                return posts
        else:
            pass

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_paginated_response(self, data):
        return Response(data)