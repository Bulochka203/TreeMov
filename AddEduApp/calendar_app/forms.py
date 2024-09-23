from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    # title = forms.CharField()
    # start_time = forms.DateTimeField()
    # end_time = forms.DateTimeField()
    # every_week = forms.BooleanField()
    template_name = 'calendar/create_event_form.html'

    class Meta:
        model = Event
        fields = ['title', 'group', 'start_time', 'end_time', 'every_week']
    #     widgets = {
    #         'title': forms.CharField(),
    #         'start_time': forms.DateTimeField(),
    #         'end_time': forms.DateTimeField(),
    #         'every_week': forms.BooleanField(),
    #     }