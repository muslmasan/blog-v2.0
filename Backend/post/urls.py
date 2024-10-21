from django.urls import path
from .views import PostDetailView, PostListView, PostCreateView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/created/', PostCreateView.as_view(), name='post-create')
]
