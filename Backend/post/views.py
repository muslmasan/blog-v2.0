from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics , viewsets
from.serializers import PostSerializer 
from .models import Post
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

class PostDetailView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

class PostCreateView(generics.CreateAPIView):
     queryset = Post.objects.all()
     permission_classes = [IsAuthenticated]
     serializer_class = PostSerializer