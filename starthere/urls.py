from django.urls import path, reverse
from django.contrib.auth.views import (
	login, logout, password_reset, password_reset_done, password_reset_confirm,
	password_reset_complete
)
from . import views

app_name = 'starthere'
urlpatterns = [
	path('', views.index, name='index'),
	path('login/', login, {'template_name': 'starthere/login.html'}, name='login'),
	path('logout/', logout, {'template_name': 'starthere/logout.html'}, name='logout'),
	path('register/', views.register, name='register'),
	path('register/activation-email/', views.account_activation_sent, name='activation_sent'),
	path('activate/<uidb64>/<token>/', views.account_activate, name='activate'),
	path('login/reset-password/', password_reset, name='password_reset'),
	path('reset-password/done/', password_reset_done, name='password_reset_done'),
	path('reset-password/confirm/<uidb64>-<token>/',
	password_reset_confirm, name='password_reset_confirm'),
	path('reset-password/confirm/complete/', password_reset_complete,
	name='password_reset_complete.html'),
	]
