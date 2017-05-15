from django.conf.urls import url
from jobs import views

urlpatterns = [
    url(r'^hello/$', views.hello_world)
]