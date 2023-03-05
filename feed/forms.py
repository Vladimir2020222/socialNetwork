from django import forms

from feed.models import Post, Image, Comment


class CreatePostFrom(forms.ModelForm):
    """Creates a post and images for this post"""

    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    def __init__(self, *args, request, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.images_list = self.request.FILES.getlist('images')

    class Meta:
        model = Post
        fields = ['title', 'text']

    def _save_m2m(self):
        super()._save_m2m()
        self.save_images()

    def save_images(self):
        Image.objects.bulk_create(
            [Image(post=self.instance, img=img) for img in reversed(self.images_list)]
        )


class UpdatePostFrom(CreatePostFrom):
    """Updates a post. Deletes old images and adds new if they are provided, otherwise doesn't delete old"""

    def _save_m2m(self):
        if self.images_list:
            self.instance.images.all().delete()
        super()._save_m2m()


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


class FormNameInput(forms.HiddenInput):
    """Used by MultipleFormMixin to determine current form when POST request has sent"""
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['name'] = 'form_name'
        return context
