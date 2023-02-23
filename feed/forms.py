from django import forms

from feed.models import Post, Image


class CreatePostFrom(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True, 'required': False}))

    def __init__(self, *args, request, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = Post
        fields = ['title', 'text']

    def _save_m2m(self):
        super()._save_m2m()
        Image.objects.bulk_create(
            [Image(post=self.instance, img=img) for img in self.request.FILES.getlist('images')]
        )


class UpdatePostFrom(CreatePostFrom):
    def _save_m2m(self):
        self.instance.images.all().delete()
        super()._save_m2m()
