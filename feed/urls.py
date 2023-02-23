from django.urls import path
from feed.views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='main')
]
