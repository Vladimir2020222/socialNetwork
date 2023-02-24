from django.conf import settings


def main_menu(request):
    return {'main_menu': settings.MAIN_MENU_LINKS}
