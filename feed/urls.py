from django.urls import path
from feed.views import MainView, CreatePostView, UpdatePostView, PostDetailView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('create_post', CreatePostView.as_view(), name='post_create'),
    path('update_post/<int:pk>', UpdatePostView.as_view(), name='post_update')
]
