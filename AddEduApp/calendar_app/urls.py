from django.urls import path
from . import views

app_name = "calendar_app"

urlpatterns = [
    path('', views.CalendarForMentor.as_view(), name='calendar'),
    path('get_events/<int:month>/<int:day>/<int:year>', views.get_events, name='get_events'),
    path('get_all_events/<int:month>/<int:year>', views.get_all_events, name='get_all_events'),
    path('get_event_data/<int:event_id>', views.get_event_data, name='get_event_data'),
]
