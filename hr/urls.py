from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('appointments/', views.get_appointments, name='get_hr_data'),
    path('create', views.create_appointment, name='post_hr_data'),
    path('possible_appointments', views.get_possible_appointments, name='get_possible_appointments'),
    path('delete_all', views.delete_all, name='delete_appointment'),
    #list all apis
    ]