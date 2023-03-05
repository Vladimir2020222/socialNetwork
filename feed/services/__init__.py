from enum import Enum


class LikeActions(Enum):
    like = 0
    unlike = 1
    dislike = 2
    undislike = 3


def like_or_dislike_object(obj, user, action):
    match action:
        case LikeActions.like:
            obj.dislikes.remove(user)
            obj.likes.add(user)
        case LikeActions.unlike:
            obj.likes.remove(user)
        case LikeActions.dislike:
            obj.likes.remove(user)
            obj.dislikes.add(user)
        case LikeActions.undislike:
            obj.dislikes.remove(user)
