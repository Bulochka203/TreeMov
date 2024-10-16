from django.urls import path, include
from . import views

app_name = "achievments"

urlpatterns = [
    path('', views.AllAchievments.as_view(), name='achievments_list'),
]