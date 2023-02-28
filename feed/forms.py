from django import forms

from feed.models import Post, Image, Comment


class CreatePostFrom(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    def __init__(self, *args, request, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = Post
        fields = ['title', 'text']

    def _save_m2m(self):
        super()._save_m2m()
        Image.objects.bulk_create(
            [Image(post=self.instance, img=img) for img in reversed(self.request.FILES.getlist('images'))]
        )


class UpdatePostFrom(CreatePostFrom):
    def _save_m2m(self):
        self.instance.images.all().delete()
        super()._save_m2m()


class CommentForm(forms.Form):
    text = forms.CharField()

    def __init__(self, data=None, post=None, *args, request=None, **kwargs):
        super().__init__(data=data, *args, **kwargs)
        if post is None:
            attrs = {}
        else:
            attrs = {'value': post.pk}
        self.fields['post'] = forms.ModelChoiceField(Post.objects, widget=forms.HiddenInput(attrs=attrs))
        self.post = post or Post.objects.get(pk=data['post'])
        self.request = request

    def save(self):
        if self.request is None:
            raise ValueError('impossible to save a form because request was not passed to __init__')
        Comment.objects.create(author=self.request.user, post=self.post, text=self.cleaned_data['text'])


class FormNameInput(forms.HiddenInput):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['name'] = 'form_name'
        return context
