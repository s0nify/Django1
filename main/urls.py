from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add_new_service', views.add_new_service),
    path('check_services', views.check_services),
    path('remove_service', views.remove_service),
    path('change_selected_service', views.change_selected_service),
    path('team/get_employees', views.get_employees),
    path('changePhone', views.changePhone)
]