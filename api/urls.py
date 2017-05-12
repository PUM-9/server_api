from django.conf.urls import url
from api import views

urlpatterns = [
    url(r'^register/$', views.create_register_job)
]
