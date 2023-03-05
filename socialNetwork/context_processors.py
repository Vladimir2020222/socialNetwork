from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.conf import settings


def main_menu(request):
    return {'main_menu': [(reverse(link), _(name)) for link, name in settings.MAIN_MENU_LINKS]}
