from django.urls import path, include
from . import views

app_name = "user_profile"

urlpatterns = [
    path('mentor', views.ProfileForMentor.as_view(), name='mentor_profile'),
    path('dashboard_groups', views.MentorDashboard.as_view(), name='mentor_groups'),
    path('admin', views.ProfileForPersonal.as_view(), name='personal_profile'),
    path('student', views.ProfileForStudent.as_view(), name='student_profile'),
    path('validate_group_name', views.validate_username, name='validate_group_name'),
    path('mentor/<str:name>/<int:pk>', views.GroupDetail.as_view(), name='group_detail'),
    path('group/<str:name>/<int:pk>', views.invite_group, name='invite_group_link'),
    path('get_photo', views.get_photo, name='get_photo'),
    path('repulse_the_attack/', views.repulse_the_attack, name='repulse_the_attack'),
    path('tree_stage_progress/', views.tree_stage_progress, name='tree_stage_progress'),
    path('plant_tree/', views.plant_tree, name='plant_tree'),
    path('create_report/', views.create_report, name='create_report'),
    path('collect_coins/', views.collect_coins, name='collect_coins'),
]