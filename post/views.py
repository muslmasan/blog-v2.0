from rest_framework import generics
from.serializers import PostSerializer
from .models import Post
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated

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