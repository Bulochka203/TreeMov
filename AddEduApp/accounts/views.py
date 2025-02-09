from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.urls import reverse
from .forms import SignInForm, SignUpForm
from .models import User
from .models.teacher_codes import TeacherCode
from user_profile.models import MentorProfile, StudentProfile, PersonalProfile, PlayerStatistics, CounterOfBusters
from shop.models import Buster


def Entrance(request):
    return render(request, 'accounts/entrance.html')


class SignInView(View):
    """ Интерфейс логин-формы"""
    template_name = "accounts/signin.html"
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form, "role": request.GET.get("role")}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Здесь использовал более джанговский вариант, ибо кастомный не проходит аутентификацию
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                if user.is_teacher and not user.is_staff:
                    return redirect("user_profile:mentor_profile")
                elif user.is_staff and not user.is_teacher:
                    return redirect("user_profile:personal_profile")
                else:
                    return redirect("user_profile:student_profile")
            else:
                messages.error(request, "Неверный email или пароль.")
        context = {"form": form}
        return render(request, "accounts/entrance.html", context)


class SignUpView(View):
    """ Интерфейс регстрации """

    template_name = "accounts/signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        error = request.GET.get("error")
        role = request.GET.get("role")
        context = {"form": form, "role": role, "error": error}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        role = request.GET.get("role")
        print(f" ВАША РООООЛЬ - {role}")

        if form.is_valid():
            first_name = form.cleaned_data.get("first_name", "").strip()
            last_name = form.cleaned_data.get("last_name", "").strip()
            print(f"ВАШЕ ИМЯЯЯ --- {first_name}")
            print(f"ВАША ФАМИЛИЯ --- {last_name}")

            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = form.save(commit=False)

            if role == 'teacher':
                user.is_teacher = True
            elif role == 'student':
                user.is_teacher = False
                user.is_staff = False
            else:
                user.is_staff = True
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                if role == 'teacher':
                    MentorProfile.objects.create(
                        user=user, first_name=first_name, last_name=last_name)
                    return redirect("user_profile:mentor_profile")
                elif role == 'student':
                    statistics = PlayerStatistics.objects.create()
                    student = StudentProfile.objects.create(
                        user=user, first_name=first_name, last_name=last_name, statistics=statistics
                    )
                    for buster in Buster.objects.all():
                        CounterOfBusters.objects.create(
                            student=student, buster=buster, count=2)
                    return redirect("user_profile:student_profile")
                else:
                    PersonalProfile.objects.create(
                        user=user, first_name=first_name, last_name=last_name)
                    return redirect("user_profile:personal_profile")

        context = {"form": form}
        return render(request, self.template_name, context)


class TeacherCodeView(View):
    """ Представление для ввода кода преподавателя """

    template_name = "accounts/teacherCode.html"

    def get(self, request, *args, **kwargs):
        teacher_code = request.GET.get("code")
        context = {"teacher_code": teacher_code}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        teacher_code = request.POST.get("teacher_code")
        if teacher_code:
            if TeacherCode.objects.filter(code=teacher_code).exists():

                # Если что --> reverse - для построения url с параметрами
                url = reverse('accounts:signin') + \
                    f"?role=teacher&teacher_code={teacher_code}"
                return HttpResponseRedirect(url)
            else:
                messages.error(request, "Неверный код преподавателя.")
                context = {"error": "Неверный код преподавателя"}
        else:
            context = {"error": "Пожалуйста, введите код преподавателя."}
        return render(request, self.template_name, context)


class CreateTeacherCodeView(View):
    """ Создает темплейт для создания кода препода """

    template_name = "accounts/createTeacherCode.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        teacher_code = request.POST.get("teacher_code")
        if teacher_code:
            TeacherCode.objects.create(code=teacher_code)
            url = reverse('accounts:signup') + \
                f"?role=teacher&teacher_code={teacher_code}"
            return HttpResponseRedirect(url)
        return render(request, self.template_name)


def redirect_to(request):
    if request.COOKIES:
        if request.user.is_authenticated:
            print(0)
            if hasattr(request.user, 'mentorprofile'):
                print(1)
                return redirect('user_profile:mentor_profile')
            elif hasattr(request.user, 'studentprofile'):
                print(2)
                return redirect('user_profile:student_profile')
            elif hasattr(request.user, 'personalprofile'):
                print(3)
                return redirect('user_profile:personal_profile')
            else:
                return HttpResponseBadRequest()
        else:
            return redirect('accounts:entrance')
    else:
        return redirect('accounts:signinBase')


@login_required
def signout(request):
    logout(request)
    return redirect("accounts:entrance")   # Пока вернул в самое начало
