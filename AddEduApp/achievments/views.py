from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Achievements


class AllAchievments(LoginRequiredMixin, ListView):
    model = Achievements
    raise_exception = True
    template_name = "achievements/achievements.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.studentprofile

        context["title"] = 'Достижения'
        context['money'] = student.balance
        context['evenrgy'] = student.energy

        return context

