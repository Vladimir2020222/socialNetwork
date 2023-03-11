from django.urls import path

from feed.services import LikeActions
from feed.views import main, subscriptions, CreatePostView, UpdatePostView, PostDetailView, DeletePostView
from feed.views.ajax import PostLikeAjaxView, CommentLikeAjaxView, send_comment, send_answer_to_comment, \
    get_post_comments, subscribe, unsubscribe, add_post_to_viewed, get_additional_posts


urlpatterns = [
    path('', main, name='main'),
    path('subscriptions', subscriptions, name='subscriptions'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post'),
    path('create_post', CreatePostView.as_view(), name='post_create'),
    path('update_post/<int:pk>', UpdatePostView.as_view(), name='post_update'),
    path('delete_post/<int:pk>', DeletePostView.as_view(), name='post_delete'),
    # post likes
    path('like_post', PostLikeAjaxView.as_view(action=LikeActions.like), name='like_post'),
    path('unlike_post', PostLikeAjaxView.as_view(action=LikeActions.unlike), name='unlike_post'),
    path('dislike_post', PostLikeAjaxView.as_view(action=LikeActions.dislike), name='dislike_post'),
    path('undislike_post', PostLikeAjaxView.as_view(action=LikeActions.undislike), name='undislike_post'),
    # comment likes
    path('like_comment', CommentLikeAjaxView.as_view(action=LikeActions.like), name='like_comment'),
    path('unlike_comment', CommentLikeAjaxView.as_view(action=LikeActions.unlike), name='unlike_comment'),
    path('dislike_comment', CommentLikeAjaxView.as_view(action=LikeActions.dislike), name='dislike_comment'),
    path('undislike_comment', CommentLikeAjaxView.as_view(action=LikeActions.undislike), name='undislike_comment'),

    path('subscribe', subscribe, name='subscribe'),
    path('unsubscribe', unsubscribe, name='unsubscribe'),

    path('get_post_comments', get_post_comments, name='get_post_comments'),
    path('send_comment', send_comment, name='send_comment'),
    path('send_answer_to_comment', send_answer_to_comment, name='send_answer_to_comment'),
    path('add_post_to_viewed', add_post_to_viewed, name='add_post_to_viewed'),
    path('get_additional_posts', get_additional_posts, name='get_additional_posts')
]
