from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.Shop.as_view(), name='main_page_shop'),
    path('get_balance', views.Shop.as_view(), name='get_balance'),
]
