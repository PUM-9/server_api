from django.conf.urls import url
from frontend import views

urlpatterns = [
    url(r'^create_registration_job/$', views.registration_job_form, name='create_registration_job'),
    url(r'^show_registration_job/$', views.registration_job_show, name='show_registration_job'),
    url(r'', views.index, name='home')
]

