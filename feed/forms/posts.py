from django import forms

from feed.models import Post, Image


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
