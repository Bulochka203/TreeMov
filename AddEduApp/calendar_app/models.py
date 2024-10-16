from datetime import datetime
from django.db import models
from user_profile.models import Group


class AbstractModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventQuerySet(models.QuerySet):
    def get_events_by_date_and_groups(self, date, groups):
        return self.filter(start_time__date=date, group__in=groups, is_active=True, is_deleted=False, every_week=False)

    def get_events_by_date_and_groups_weekly(self, date, groups):
        return self.filter(start_time__date=date, group__in=groups, is_active=True, is_deleted=False)

    def get_event_dates_in_current_month_and_year(self, month, year, groups):
        return self.filter(start_time__month=month, start_time__year=year, every_week=False,
                           group__in=groups, is_active=True, is_deleted=False).dates('start_time', 'day')

    def get_every_week_events(self, groups):
        return self.filter(group__in=groups, is_active=True, is_deleted=False, every_week=True)


class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model)

    def get_events_by_date_and_groups(self, date, groups):
        return self.get_queryset().get_events_by_date_and_groups(date, groups)

    def get_event_dates_in_current_month_and_year(self, month, year, groups):
        return self.get_queryset().get_event_dates_in_current_month_and_year(month, year, groups)

    def get_every_week_events(self, groups):
        return self.get_queryset().get_every_week_events(groups)

    def get_events_by_date_and_groups_weekly(self, date, groups):
        return self.get_queryset().get_events_by_date_and_groups_weekly(date, groups)


class Event(AbstractModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="events")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    every_week = models.BooleanField()

    objects = models.Manager()
    event_manager = EventManager()

    def __str__(self):
        return self.title

    def template_output(self):
        return {
            'event_pk': self.pk,
            'title': self.title,
            'time': f'{datetime.strftime(self.start_time, "%H:%M")} - {datetime.strftime(self.end_time, "%H:%M")}',
            'group': self.group.name,
            'date': datetime.strftime(self.start_time, "%Y-%m-%d"),
            'every_week': self.every_week,
        }


class ExceptionDaysQuerySet(models.QuerySet):
    def get_all_exceptions_for_event(self, events, month):
        return self.filter(event__in=events, date__month=month, is_active=True, is_deleted=False)\
            .dates('date', 'day')


class ExceptionDaysManager(models.Manager):
    def get_queryset(self):
        return ExceptionDaysQuerySet(self.model)

    def get_all_exceptions_for_event(self, events, month):
        return self.get_queryset().get_all_exceptions_for_event(events, month)


class ExceptionDays(AbstractModel):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="exceptions")
    date = models.DateField()

    objects = models.Manager()
    exception_days_manager = ExceptionDaysManager()
