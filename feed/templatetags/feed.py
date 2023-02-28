from django import template
from django.contrib.auth.models import User

from feed.models import Post

register = template.Library()


@register.filter(name='has_liked_by')
def has_liked_by(post: Post, user: User):
    if user.is_anonymous:
        return False
    return post.likes.contains(user)


@register.filter(name='has_disliked_by')
def has_disliked_by(post: Post, user: User):
    if user.is_anonymous:
        return False
    return post.dislikes.contains(user)
