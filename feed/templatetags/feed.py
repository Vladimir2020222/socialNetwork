from django import template
from django.contrib.auth.models import User

from feed.models import LikeablePermission

register = template.Library()


@register.filter
def has_liked_by(model: LikeablePermission, user: User):
    if user.is_anonymous:
        return False
    return model.likes.contains(user)


@register.filter
def has_disliked_by(model: LikeablePermission, user: User):
    if user.is_anonymous:
        return False
    return model.dislikes.contains(user)


@register.filter
def render_with_request(obj, request):
    return obj.render(request=request)
