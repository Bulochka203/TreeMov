from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View

from .forms import SignInForm, SignUpForm
from .models.teacher_codes import TeacherCode


class SignInView(View):
    """ User registration view """

    template_name = "accounts/signin.html"
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data["email"]
            password = forms.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if user.is_teacher:
                    return redirect(f"user_profile:mentor_profile")
                elif user.is_staff:
                    return redirect(f"user_profile:personal_profile")
                else:
                    return redirect(f"user_profile:student_profile")
        context = {"form": forms}
        return render(request, self.template_name, context)


class SignUpView(View):
    """ User registration view """

    template_name = "accounts/signup.html"
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if user.is_teacher:
                    return redirect(f"user_profile:mentor_profile")
                elif user.is_staff:
                    return redirect(f"user_profile:personal_profile")
                else:
                    return redirect(f"user_profile:student_profile")
            return redirect("accounts:signin")
        context = {"form": form}

        return render(request, self.template_name, context)


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
            return redirect('accounts:signup')
    else:
        return redirect('accounts:signin')


@login_required
def signout(request):
    logout(request)
    return redirect("accounts:signin")