from django.urls import reverse
from django.conf import settings


class MainMenuLink:
    def __init__(self, url_name, title, auth=None):
        self.url_name = url_name
        self.title = title
        self.auth = auth

    def should_show(self, request):
        if self.auth is None:
            return True
        return request.user.is_authenticated == self.auth

    def resolve(self):
        return [reverse(self.url_name), self.title]


def main_menu(request):
    return {'main_menu': [link.resolve() for link in settings.MAIN_MENU_LINKS if link.should_show(request)]}
