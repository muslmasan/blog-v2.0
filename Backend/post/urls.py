from django.urls import path
from .views import PostDetailView, PostListCreateView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail')
]
