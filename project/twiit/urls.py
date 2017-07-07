from django.conf.urls import url

from project.twiit import views


app_name = 'twiit'
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
]