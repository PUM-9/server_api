from django.conf.urls import url
from frontend import views

urlpatterns = [
    url(r'^create_registration_job/$', views.registration_job_form, name='create_registration_job'),
    url(r'^create_mesh_job/$', views.mesh_job_form, name='create_mesh_job'),
    url(r'^start_registration/([0-9]*)$', views.start_registration, name='start_registration'),
    url(r'^show_job/$', views.show_job, name='show_job'),
    url(r'^delete_job/$', views.delete_job, name='delete_job'),
    url(r'', views.index, name='index')
]

