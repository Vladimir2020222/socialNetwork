from django import forms

from feed.models import Post, Comment


class BaseCommentForm(forms.Form):
    """Base form for CommentForm and AnswerForm"""

    text = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Написать комментарий', 'class': 'comment-input', 'cols': '65', 'rows': '2'}
    ))

    post = forms.ModelChoiceField(Post.objects, widget=forms.HiddenInput)


class CommentForm(BaseCommentForm):
    """Form to comment a post"""

    def __init__(self, data=None, post=None, request=None, *args, **kwargs):
        super().__init__(data=data, *args, **kwargs)
        if post is not None:
            self.fields['post'].widget.attrs['value'] = post.pk

        self.post = post or Post.objects.get(pk=data[self.add_prefix('post')])
        self.request = request

    def save(self):
        if self.request is None:
            raise ValueError('impossible to save a form because request was not passed to __init__')
        Comment.objects.create(author=self.request.user, post=self.post, text=self.cleaned_data['text'])


class AnswerForm(BaseCommentForm):
    """Form to answer comments"""

    answer_to = forms.ModelChoiceField(Comment.objects, widget=forms.HiddenInput)

    def __init__(self, data=None, post=None, request=None, answer_to=None, *args, **kwargs):
        super().__init__(data=data, *args, **kwargs)
        if post is not None:
            self.fields['post'].widget.attrs['value'] = post.pk

        if answer_to is not None:
            self.fields['answer_to'].widget.attrs['value'] = answer_to.pk
            username = answer_to.author.username
            self.fields['text'].widget.attrs['placeholder'] = 'Ответить на комментарий %s' % (username, )

        self.post = post or Post.objects.get(pk=data[self.add_prefix('post')])
        self.answer_to = answer_to or Comment.objects.get(pk=data[self.add_prefix('answer_to')])
        self.request = request

    def save(self):
        if not self.is_valid():
            raise ValueError('form is not valid, impossible to save it')
        if self.request is None:
            raise ValueError('impossible to save a form because request was not passed to __init__')
        Comment.objects.create(author=self.request.user,
                               post=self.post,
                               text=self.cleaned_data['text'],
                               answer_to=self.answer_to)