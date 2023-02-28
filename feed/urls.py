from django.http import HttpResponse
from django.urls import path
from feed.views import MainView, CreatePostView, UpdatePostView, PostDetailView, DeletePostView, PostLikeAjaxView, \
    PostLikeActions, send_comment


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('create_post', CreatePostView.as_view(), name='post_create'),
    path('update_post/<int:pk>', UpdatePostView.as_view(), name='post_update'),
    path('delete_post/<int:pk>', DeletePostView.as_view(), name='post_delete'),
    path('like_post', PostLikeAjaxView.as_view(action=PostLikeActions.like), name='like_post'),
    path('unlike_post', PostLikeAjaxView.as_view(action=PostLikeActions.unlike), name='unlike_post'),
    path('dislike_post', PostLikeAjaxView.as_view(action=PostLikeActions.dislike), name='dislike_post'),
    path('undislike_post', PostLikeAjaxView.as_view(action=PostLikeActions.undislike), name='undislike_post'),
    path('send_comment', send_comment, name='send_comment')
]
