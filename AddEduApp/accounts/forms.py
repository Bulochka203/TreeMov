from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User
from .models.teacher_codes import TeacherCode, AdminCode
from .validators import validate_name
from shop.models import Buster
from user_profile.models import MentorProfile, PlayerStatistics, StudentProfile, CounterOfBusters, PersonalProfile


class SignInForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input-data", 'placeholder': 'ФИО'}),
        validators=[validate_name],
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "input-data", 'placeholder': 'email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "input-data", 'placeholder': 'Пароль'})
    )


class SignUpForm(forms.ModelForm):
    full_name = forms.CharField(
        label=" Имя",
        widget=forms.TextInput(
            attrs={"class": "input-data", 'placeholder': 'ФИО'}),
        validators=[validate_name],
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "input-data", 'placeholder': 'email'}),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "input-data", 'placeholder': 'Придумайте пароль'}),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(
            attrs={"class": "input-data", 'placeholder': 'Повторите пароль'}),
        validators=[validate_password],
    )
    teacher_code = forms.CharField(
        label="Код преподавателя",
        widget=forms.TextInput(attrs={
                               "class": "input-data", 'id': 'teacher-code', 'placeholder': 'Код преподавателя'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ["full_name", "email"]
        widgets = {"email": forms.EmailInput(
            attrs={"class": "input-data", 'placeholder': 'email'})}

    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get("full_name", "").strip()
        name_parts = full_name.split()

        if len(name_parts) > 1:
            cleaned_data["first_name"] = " ".join(name_parts[1:])
            cleaned_data["last_name"] = name_parts[0]
        else:
            cleaned_data["first_name"] = full_name
            cleaned_data["last_name"] = ""

        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            self.add_error("password2", "Пароли не совпадают")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        is_teacher = False
        is_admin = False
        if teacher_code := self.cleaned_data["teacher_code"]:
            is_teacher = TeacherCode.objects.filter(code=teacher_code).exists()
            is_admin = AdminCode.objects.filter(code=teacher_code).exists()

        if commit:
            if is_teacher:
                user.is_teacher = True
            if is_admin:
                user.is_staff = True
            user.save()

            if user.is_teacher:
                MentorProfile.objects.create(
                    first_name=self.cleaned_data["full_name"], user=user)
            elif user.is_staff:
                PersonalProfile.objects.create(
                    first_name=self.cleaned_data["full_name"], user=user)
            else:
                statistics = PlayerStatistics()
                statistics.save()
                student = StudentProfile.objects.create(
                    first_name=self.cleaned_data["full_name"], user=user, statistics=statistics)
                for buster in Buster.objects.all():
                    CounterOfBusters.objects.create(
                        student=student, buster=buster, count=2)
        return user
