from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User
from .models.teacher_codes import TeacherCode
from .validators import validate_name
from shop.models import Buster
from user_profile.models import MentorProfile, PlayerStatistics, StudentProfile, CounterOfBusters


class SignInForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "input-data", 'placeholder': 'email'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input-data", 'placeholder': 'Пароль'})
    )


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={"class": "input-data", 'placeholder': 'Имя'}),
        validators=[validate_name],
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={"class": "input-data", 'placeholder': 'Фамилия'}),
        validators=[validate_name],
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "input-data", 'placeholder': 'Пароль'}),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Подтвердите пароль",
        widget=forms.PasswordInput(attrs={"class": "input-data", 'placeholder': 'Повторите пароль'}),
        validators=[validate_password],
    )
    teacher_code = forms.CharField(
        label="Код преподавателя",
        widget=forms.TextInput(attrs={"class": "input-data", 'id': 'teacher-code', 'placeholder': 'Код преподавателя'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ["email"]
        widgets = {"email": forms.EmailInput(attrs={"class": "input-data", 'placeholder': 'email'})}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password didn't match!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        is_teacher = False
        if teacher_code := self.cleaned_data["teacher_code"]:
            is_teacher = TeacherCode.objects.filter(code=teacher_code).exists()

        if commit:
            if is_teacher:
                user.is_teacher = True

            user.save()

            if user.is_teacher:
                MentorProfile.objects.create(first_name=self.cleaned_data["first_name"],
                                             last_name=self.cleaned_data["last_name"], user=user)
            else:
                statistics = PlayerStatistics()
                statistics.save()
                student = StudentProfile.objects.create(first_name=self.cleaned_data["first_name"],
                                                        last_name=self.cleaned_data["last_name"],
                                                        user=user, statistics=statistics)
                for buster in Buster.objects.all():
                    CounterOfBusters.objects.create(student=student, buster=buster, count=2)
        return user
