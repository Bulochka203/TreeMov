from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.redirect_to, name='redirect'),
    path("entrance/", views.Entrance, name="entrance"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("signout/", views.signout, name="signout"),
    path("teacher-code/", views.TeacherCodeView.as_view(), name="teacherCode"),
    path("create-teacher-code/", views.CreateTeacherCodeView.as_view(),
         name="create_teacher_code"),
]
