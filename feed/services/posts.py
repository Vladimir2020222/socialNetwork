import warnings

from django.db.models import QuerySet, Manager
from django.contrib.auth.models import AbstractBaseUser

from feed.models import Post
import random


class SortedPostsWrapper(list):
    def __getattr__(self, item):
        raise AttributeError("'%s' object has no attribute '%s'. May be you try to use this list of posts "
                             "as queryset." % (self.__class__.__qualname__, item))


def sort_posts_by_relevance_with_shuffle(posts: QuerySet | Manager) -> SortedPostsWrapper:
    if isinstance(posts, Manager):
        posts = posts.all()

    if len(posts) > 5000:
        raise OverflowError('too many posts, sorting may take very much time and memory')

    posts = list(posts.sort_by_relevance())

    for _ in range(len(posts)//10+1):
        for i in range(len(posts)):
            if random.random() < 0.2:
                if random.randint(0, 1):
                    if i + 1 < len(posts):
                        posts[i], posts[i + 1] = posts[i + 1], posts[i]
                else:
                    if i != 0:
                        posts[i - 1], posts[i] = posts[i], posts[i - 1]
    posts = SortedPostsWrapper(posts)
    return posts


def get_subscriptions_posts(user, posts=None):
    if posts is None:
        posts = Post.objects
    subscriptions = user.subscriptions.only('pk')
    return posts.all().filter(author__in=subscriptions).order_by('-date_published')


def get_random_subscriptions_posts(user: AbstractBaseUser, posts=None, n=10, exclude_viewed=False) -> list:
    return get_random_posts(get_subscriptions_posts(user, posts), n, user=user, exclude_viewed=exclude_viewed)


def get_random_posts(posts: QuerySet | Manager = None,
                     n=10, user: AbstractBaseUser = None,
                     exclude_viewed=True,
                     exclude_posts_by_current_user=True) -> list:
    if exclude_viewed and not user:
        raise ValueError('impossible to exclude viewed posts without user. '
                         'Pass user to get_random_posts or set exclude_viewed to False')
    if n > 1000:
        raise OverflowError("you shouldn't select more than 1000 posts")

    if posts is None:
        posts = Post.objects.select_related()

    if not user.is_anonymous:
        if exclude_viewed:
            posts = posts.exclude_viewed(user)
        if exclude_posts_by_current_user:
            posts = posts.exclude(author_id=user.pk)

    posts = sort_posts_by_relevance_with_shuffle(posts)

    if not posts:
        return []
    if len(posts) <= n:
        return posts

    sorted_posts = []
    cycle_n = 0
    while len(sorted_posts) < n:
        slice_end = len(posts)
        for _ in range(len(posts) // 10 + 1):
            slice_end = random.randint(0, slice_end)
        slice_end = slice_end or 1
        sliced = posts[0:slice_end]

        possible_choices = sliced.copy()
        for added_post in sorted_posts:
            if added_post in possible_choices:
                possible_choices.pop(possible_choices.index(added_post))
        if not sliced:
            continue
        post = random.choice(sliced)
        if post not in sorted_posts:
            sorted_posts.append(post)
        cycle_n += 1
        if cycle_n > 1000:
            warnings.warn('mixing algorithm iterated 1000 times, it may take too many time and memory', stacklevel=2)

    return sorted_posts
