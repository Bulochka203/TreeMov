from datetime import datetime
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView
from itertools import chain

from .forms import EventForm
from .models import Event, ExceptionDays
from user_profile.models import Group


class CalendarForMentor(LoginRequiredMixin, ListView):
    raise_exception = True
    template_name = "calendar/calendar.html"
    model = Event

    def get(self, request, *args, **kwargs):
        if hasattr(request.user, 'studentprofile'):
            profile_id = request.user.studentprofile
            groups = Group.objects.filter(students=profile_id.pk)
        elif hasattr(request.user, 'mentorprofile'):
            profile_id = request.user.mentorprofile
            groups = Group.objects.filter(mentors=profile_id.pk)
        else:
            return Http404

        groups_pk_list = [group.pk for group in groups]
        curr_date = datetime.now().date()
        event_list = Event.event_manager.get_events_by_date_and_groups_weekly(curr_date, groups_pk_list)

        context = {
            'groups': groups,
            'title': 'Календарь',
            'event_list': [event.template_output() for event in event_list]
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'studentprofile'):
            return HttpResponseForbidden()
        if 'event_pk' in request.POST:
            delete_every_week = False
            if 'every-week' in request.POST:
                delete_every_week = True
            event_pk = request.POST.get('event_pk')
            delete_date = request.POST.get('delete-date')
            event = Event.objects.get(pk=event_pk)
            if event.every_week and not delete_every_week:
                ExceptionDays.objects.create(
                    event=event,
                    date=datetime.strptime(f'{delete_date}', '%d-%m-%Y').date(),
                )
            else:
                event.delete()
        elif 'select-group' in request.POST:
            group_pk = request.POST.get('select-group')
            start_time = request.POST.get('start-time')
            end_time = request.POST.get('end-time')
            event_title = request.POST.get('event-title')
            event_date = request.POST.get('date')
            every_week = request.POST.get('every-week-checkbox')
            event_pk = request.POST.get('updated-event-pk')

            start_time = datetime.strptime(f'{event_date} {start_time}', '%Y-%m-%d %H:%M')
            end_time = datetime.strptime(f'{event_date} {end_time}', '%Y-%m-%d %H:%M')

            if event_pk.isdigit():
                print('update')
                print(every_week)
                print(True if every_week == '1' else False)
                Event.objects.filter(pk=int(event_pk)).update(
                    title=event_title,
                    group=Group.objects.get(pk=group_pk),
                    start_time=start_time,
                    end_time=end_time,
                    every_week=True if every_week == '1' else False
                )
            else:
                print('create')
                Event.objects.create(
                    title=event_title,
                    group=Group.objects.get(pk=group_pk),
                    start_time=start_time,
                    end_time=end_time,
                    every_week=True if every_week == '1' else False
                )

        return redirect('calendar_app:calendar')


@login_required
def get_events(request, month, day, year):
    if request.method != "GET":
        return HttpResponseBadRequest
    elif hasattr(request.user, 'studentprofile'):
        profile_id = request.user.studentprofile
        groups = Group.objects.filter(students=profile_id.pk)
    elif hasattr(request.user, 'mentorprofile'):
        profile_id = request.user.mentorprofile
        groups = Group.objects.filter(mentors=profile_id.pk)
    else:
        return Http404

    groups_pk_list = [group.pk for group in groups]

    curr_date = date(year, month, day)
    event_list = Event.event_manager.get_events_by_date_and_groups(curr_date, groups_pk_list)
    every_week_events = Event.event_manager.get_every_week_events(groups_pk_list)

    event_list = [event.template_output() for event in event_list]

    curr_weekday = curr_date.isoweekday()
    for event in every_week_events:
        if event.start_time.isoweekday() == curr_weekday and not event.exceptions.filter(
                date=curr_date, is_active=True, is_deleted=False).exists():
            event_list.append(event.template_output())

    response = {
        'events': event_list
    }

    return JsonResponse(response)


@login_required
def get_all_events(request, month, year):
    if request.method != "GET":
        return HttpResponseBadRequest
    elif hasattr(request.user, 'studentprofile'):
        profile_id = request.user.studentprofile
        groups = Group.objects.filter(students=profile_id.pk)
    elif hasattr(request.user, 'mentorprofile'):
        profile_id = request.user.mentorprofile
        groups = Group.objects.filter(mentors=profile_id.pk)
    else:
        return Http404

    groups_pk_list = [group.pk for group in groups]

    event_list = Event.event_manager.get_event_dates_in_current_month_and_year(month, year, groups_pk_list)
    every_week_events = Event.event_manager.get_every_week_events(groups_pk_list)
    exception_days_querries = ExceptionDays.\
        exception_days_manager.\
        get_all_exceptions_for_event([event.pk for event in every_week_events], month)

    response = {
        'week_days': [0 if event.start_time.isoweekday() == 7 else event.start_time.isoweekday() for event in every_week_events],
        'dates': [event_data.day for event_data in event_list],
        'exceptions': [exception_day.day for exception_day in exception_days_querries],
    }
    print(response)

    return JsonResponse(response)


@login_required
def get_event_data(request, event_id):
    if hasattr(request.user, 'studentprofile'):
        return HttpResponseForbidden
    elif hasattr(request.user, 'mentorprofile'):
        pass
    elif request.method != "GET":
        return HttpResponseBadRequest
    else:
        return Http404

    event = Event.objects.get(pk=event_id)

    response = {
        'title': event.title,
        'group_pk': event.group.pk,
        'date': event.start_time.date(),
        'start_time': event.start_time,
        'end_time': event.end_time,
        'every_week': event.every_week
    }

    return JsonResponse(response)


