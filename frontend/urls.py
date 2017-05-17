from django.conf.urls import url
from frontend import views

urlpatterns = [
    url(r'^create_registration_job/$', views.registration_job_form, name='create_registration_job'),
    url(r'^show_registration_job/$', views.registration_job_show, name='show_registration_job'),
    url(r'^delete_registration_job/$', views.registration_job_delete, name='delete_registration_job'),
    url(r'^create_mesh_job/$', views.mesh_job_form, name='create_mesh_job'),
    url(r'', views.index, name='index')
]

