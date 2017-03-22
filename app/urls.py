from django.conf.urls import url
from . import views
from loginapp.views import (login_view, register_view, logout_view)

urlpatterns = [
    url(r'^$', views.index),
    url(r'^data$', views.data),
    url(r'^myview$', views.my_view),
    url(r'^login/', login_view(), name="login")
]

