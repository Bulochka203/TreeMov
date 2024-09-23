from typing import List

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render, redirect

from .models import Buster
from django.views.generic import ListView

from user_profile.models import CounterOfBusters


class Shop(LoginRequiredMixin, ListView):
    raise_exception = True
    model = Buster
    template_name = "shop/shop.html"

    def post(self, request, *args, **kwargs):
        curent_buster_pk = request.POST.get('buster-id')
        curent_buster = self.model.objects.get(pk=curent_buster_pk)
        cost = curent_buster.cost
        profile = request.user.studentprofile
        if cost < profile.energy:
            profile.energy -= cost
            student_has_buster = CounterOfBusters.objects.filter(student=profile.pk, buster=curent_buster_pk).exists()
            if not student_has_buster:
                profile.busters.add(curent_buster)
            else:
                count_busters = CounterOfBusters.objects.get(student=profile.pk, buster=curent_buster_pk)
                count_busters.count += 1
                count_busters.save()
            profile.save()
            return redirect('shop:main_page_shop')

        return HttpResponseBadRequest()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Магазин'
        return context


@login_required
def get_balance(request):
    if request.method == 'GET':
        if hasattr(request.user, 'studentprofile'):
            student = request.user.studentprofile

            response = {'balance': student.energy}

            return JsonResponse(response)
        elif hasattr(request.user, 'mentorprofile'):
            return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()