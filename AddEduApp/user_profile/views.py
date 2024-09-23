import asyncio
import datetime
import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, \
    HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from dramatiq import pipeline
from webpush.utils import send_to_subscription
from accounts.models.teacher_codes import TeacherCode, AdminCode
from .models import Achievements, MentorProfile, PersonalProfile, StudentProfile, Group, Tree, CounterOfBusters, Attendance
from .tasks import tree_progress
from .utilities import creater_report
from shop.models import Buster
from calendar_app.models import Event


class GroupDetail(LoginRequiredMixin, View):
    model = Group
    raise_exception = True
    template_name = "user_profile/group_detail.html"

    def get(self, request, *args, **kwargs):
        mentor_profile = request.user.mentorprofile
        group_pk = kwargs['pk']
        group = Group.objects.get(pk=group_pk)
        curr_date = datetime.datetime.now().date()
        event_list = Event.event_manager.get_events_by_date_and_groups_weekly(curr_date, [group_pk])

        context = {
            'data': mentor_profile,
            'group': group,
            'event_list': [event.template_output() for event in event_list]
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('student-delete'):
            student_pk = request.POST.get('student-delete')
            group_pk = kwargs['pk']

            student = StudentProfile.objects.get(pk=student_pk)
            group = Group.objects.get(pk=group_pk)
            group.students.remove(student)
        elif request.POST.get('counter'):
            counter = request.POST.get('counter')
            type_of_add = request.POST.get('add-type')
            student_pk = request.POST.get('student-add')

            student = StudentProfile.objects.get(pk=student_pk)
            group = Group.objects.get(pk=kwargs['pk'])

            attendance = Attendance.objects.filter(student=student, group=group)
            if len(attendance) == 1:
                if attendance[0].dates.count(datetime.date.today()) == 0:
                    attendance[0].dates.append(datetime.date.today())
                    attendance[0].save()
            elif len(attendance) < 1:
                Attendance.objects.create(student=student, group=group, dates=[datetime.date.today()])
            else:
                return HttpResponseServerError()

            if type_of_add == 'energy':
                student.energy += int(counter)
            elif type_of_add == 'money':
                student.balance += int(counter)
            student.save()
        return HttpResponseRedirect(reverse("user_profile:group_detail", kwargs=kwargs))


class ProfileForStudent(LoginRequiredMixin, View):
    raise_exception = True
    template_name = "user_profile/student_profile.html"

    def get(self, request):
        student = request.user.studentprofile
        achievement = Achievements.objects.all()[:2]

        payload = {"head": "Welcome!", "body": "Hello World"}
        push_infos = request.user.webpush_info.select_related("subscription")
        for push_info in push_infos:
            send_to_subscription(push_info.subscription, payload)

        busters = CounterOfBusters.objects.filter(student=student.pk)

        context = {
            "data": student,
            'tree': 0,
            "achievement": achievement,
            "models": {
                'cloud': '/models/cloud/cloud.gltf',
                'three_stage1': '/models/three_stage1/three_stage1.gltf',
                'three_stage2': '/models/three_stage2/three_stage2.gltf',
                'three_stage3': '/models/three_stage3/three_stage3.gltf',
            },
        }

        if student.tree:
            print(student.tree.stage)
            start_time = student.tree.start_time
            duration = student.tree.duration
            if start_time and duration:
                print('start_time and duration')
                if datetime.datetime.now() > start_time + duration:
                    print('datetime.datetime.now() > start_time + duration')
                    context['tree'] = 0
                else:
                    context['tree'] = student.tree.stage
            else:
                print('context["tree"] = student.tree.stage')
                context['tree'] = student.tree.stage
        print(context['tree'])

        if busters:
            context['busters'] = {
                'antimagnet': busters.get(buster__title='Антимагнит').count,
                'magicdom': busters.get(buster__title='Магический купол').count,
                'waterbucket': busters.get(buster__title='Ведро с водой').count,
            }
            context['busters_pk'] = {
                'antimagnet_pk': Buster.objects.get(title='Антимагнит').pk,
                'magicdom_pk': Buster.objects.get(title='Магический купол').pk,
                'waterbucket_pk': Buster.objects.get(title='Ведро с водой').pk,
            }

        return render(request, self.template_name, context)


class ProfileForMentor(LoginRequiredMixin, View):
    raise_exception = True
    template_name = "user_profile/mentor_profile.html"

    def post(self, request, *args, **kwargs):
        if request.POST.get('group-name-input'):
            group_name = request.POST.get('group-name-input')
            mentor_profile_id = request.user.mentorprofile
            group = Group.objects.create(name=group_name)
            group.mentors.add(mentor_profile_id)
        elif request.POST.get('group-delete'):
            group_pk = request.POST.get('group-delete')
            group = Group.objects.filter(pk=group_pk)
            group.delete()
        else:
            pass

        return redirect('user_profile:mentor_profile')

    def get(self, request, *args, **kwargs):
        mentor_profile = request.user.mentorprofile
        groups = Group.objects.filter(mentors=mentor_profile.pk)

        context = {
            'data': mentor_profile,
            'groups': groups,
        }

        return render(request, self.template_name, context)


class MentorDashboard(LoginRequiredMixin, View):
    raise_exception = True
    template_name = "user_profile/mentor_groups.html"

    def post(self, request, *args, **kwargs):
        if request.POST.get('group-name-input'):
            group_name = request.POST.get('group-name-input')
            mentor_profile_id = request.user.mentorprofile
            group = Group.objects.create(name=group_name)
            group.mentors.add(mentor_profile_id)
        elif request.POST.get('group-delete'):
            group_pk = request.POST.get('group-delete')
            group = Group.objects.filter(pk=group_pk)
            group.delete()
        else:
            pass

        return redirect('user_profile:mentor_profile')

    def get(self, request, *args, **kwargs):
        mentor_profile = request.user.mentorprofile
        groups = Group.objects.filter(mentors=mentor_profile.pk)
        

        context = {
            'data': mentor_profile,
            'groups': groups,
        }

        return render(request, self.template_name, context)
    


class ProfileForPersonal(LoginRequiredMixin, View):
    raise_exception = True
    template_name = "admin_profile/admin_profile.html"

    def get(self, request, *args, **kwargs):
        admin_profile = request.user.personalprofile

        context = {
            'data': admin_profile,
        }
        return render(request, self.template_name, context)


@login_required
def invite_group(request, name, pk):
    if request.user.is_teacher:
        return HttpResponseForbidden()

    student = request.user.studentprofile

    group = Group.objects.get(pk=pk)
    if group.students.filter(pk=student.pk):
        return HttpResponse("Вы уже состоите в данной группе")

    group.students.add(request.user.studentprofile)
    return HttpResponse("Вы успешно добавлены в группу")


@login_required
def get_photo(request):
    if request.method == 'POST':
        if hasattr(request.user, 'studentprofile'):
            user = request.user.studentprofile
            returned_view = 'user_profile:student_profile'
        elif hasattr(request.user, 'mentorprofile'):
            user = request.user.mentorprofile
            returned_view = 'user_profile:mentor_profile'
        elif hasattr(request.user, 'personalprofile'):
            user = request.user.personalprofile
            returned_view = 'user_profile:personal_profile'
        else:
            return HttpResponseBadRequest()

        pic = request.FILES.get('pic')
        user.photo = pic
        user.save()
        return redirect(returned_view)
    else:
        return HttpResponseBadRequest()


@login_required
def plant_tree(request):
    if request.method == 'GET':
        if hasattr(request.user, 'studentprofile'):
            student = request.user.studentprofile

            if not student.tree:
                tree = Tree.objects.create()
                student.tree = tree
                student.save()
                print('task create')
                tree_progress.send(student.pk)

                response = {'created': True}
            else:
                print('task not create')
                response = {'created': False}

            return JsonResponse(response)
        elif hasattr(request.user, 'mentorprofile'):
            return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@login_required
def collect_coins(request):
    if request.method == 'GET':
        if hasattr(request.user, 'studentprofile'):
            student = request.user.studentprofile

            if not student.tree:
                return HttpResponseBadRequest()
            else:
                student.tree.stage = 3
                student.tree.statistics.coins_collected += Tree.COLLECTED_COINS
                student.tree.save()

            student.balance += Tree.COLLECTED_COINS
            student.statistics.coins_collected += Tree.COLLECTED_COINS
            student.save()
            student.statistics.save()

            return JsonResponse({1: 1})
        elif hasattr(request.user, 'mentorprofile'):
            return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@login_required
def repulse_the_attack(request):
    if request.method == 'POST':
        if hasattr(request.user, 'studentprofile'):
            student = request.user.studentprofile
            buster_pk = request.POST.get('buster-pk')
            print(student.tree.stage)

            if not buster_pk:
                HttpResponseBadRequest()

            buster = CounterOfBusters.objects.get(student=student.pk, buster=buster_pk)

            response = {
                'tree_stage': 0,
                'buster_count': 0,
            }

            if student.tree:
                response['tree_stage'] = student.tree.stage

            start_time = student.tree.start_time
            duration = student.tree.duration
            if datetime.datetime.now() > start_time + duration:
                pass
                # Нe уверен, что тут нужна эта опция

            if buster.count < 1:
                return JsonResponse('Недостаточно бустеров')
            else:
                buster.count -= 1
                response['buster_count'] = buster.count
                buster.save()
                student.tree.event = None
                student.tree.start_time = None
                student.tree.save()

                # Тут надо дописать сбор статистики
                tree_progress.send(student.pk)

            return JsonResponse(response)

        elif hasattr(request.user, 'mentorprofile'):
            return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@login_required
def tree_stage_progress(request):
    if request.method == 'GET':
        if hasattr(request.user, 'studentprofile'):
            student = request.user.studentprofile

            response = {
                'tree_stage': 0,
                'negative_event': None,
                'lose_tree': False
            }

            if student.tree:
                stage = student.tree.stage
                start_time = student.tree.start_time
                duration = student.tree.duration
                event = student.tree.event

                response['tree_stage'] = stage

                if stage in [Tree.STAGES[-1][0], Tree.STAGES[-2][0]] and event in [i[0] for i in Tree.EVENTS]:
                    response['negative_event'] = Tree.EVENTS[event]

                    if datetime.datetime.now() > start_time + duration:
                        response['lose_tree'] = True
                        response['tree_stage'] = 0
                        student.tree.delete()

            return JsonResponse(response)
        elif hasattr(request.user, 'mentorprofile'):
            return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@login_required
def validate_username(request):
    mentor_profile_id = request.user.mentorprofile
    group_name = request.GET.get('group-name-input', None)
    response = {
        'is_taken': Group.objects.filter(name__iexact=group_name, mentors=mentor_profile_id).exists()
    }
    return JsonResponse(response)


@login_required
def create_report(request):
    if request.method == 'POST':
        if hasattr(request.user, 'mentorprofile'):
            mentor = request.user.mentorprofile
            groups_pk = request.POST.getlist('groups')
            dates = request.POST.get('dates')

            dates = dates.split(' - ')
            dates = list(map(lambda x: datetime.datetime.strptime(x, "%m/%d/%Y").date(), dates))

            groups = Group.objects.filter(pk__in=groups_pk)

            path_to_load = creater_report(mentor.pk, dates, groups)

            if os.path.exists(path_to_load):
                file_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                with open(path_to_load, 'rb') as fl:
                    response = HttpResponse(fl.read(), content_type=file_type, charset='utf-8')
                    response['Content-Disposition'] = f'attachment; filename={path_to_load.split("/")[-1]}'
                    response['Content-Length'] = os.path.getsize(path_to_load)
                    return response

            return HttpResponseNotFound()
        elif hasattr(request.user, 'studentprofile'):
            return HttpResponseForbidden()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()
