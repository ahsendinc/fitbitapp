from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
#from loginapp.views import (login_view, register_user, logout_view)

urlpatterns = [
    url(r'^$', views.index),
    url(r'^data$', views.data),
    url(r'^myview$', views.my_view),
    url(r'^registration$', views.register_user, name = "registration"),
    url(r'^profile2$', views.profile2, name='profile2'),
    #url(r'^accounts/login/$', auth_views.login, {'template_name': 'index.html','authentication_form': LoginForm}, name="login") ,

    url(r'^login/', views.login_view, name = "login_view")
]

