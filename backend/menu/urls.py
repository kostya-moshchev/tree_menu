from django.urls import path

from .views import IndexView


app_name = 'menu'

urlpatterns = [
    path('<str:active_item>/', IndexView.as_view(), name='menu_item')
]