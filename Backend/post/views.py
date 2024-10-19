from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics , viewsets
from.serializers import PostSerializer 
from .models import Post
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 