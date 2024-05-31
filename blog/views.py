
""" def index(request):
    return render(request, 'blog/index.html') """

# blog/views.py

from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})