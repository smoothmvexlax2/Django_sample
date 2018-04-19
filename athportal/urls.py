from django.urls import path, re_path
from . import views

app_name = 'athportal'
urlpatterns = [
	path('', views.index, name='ath_home'),
	path('createprofile/', views.professional_registration,
		name='create_professional_profile',
	),
	path('profile/', views.view_profile, name='view_profile'),
	path('profile/edit/goals/', views.edit_athlete_goals, name='edit_goals'),
	path('profile/edit/personalrecord/<movement_name>/',
		views.edit_personal_record,
		name='edit_personal_record'),
	path('profile/edit/profile', views.edit_profile, name='edit_profile'),
	path('profile/edit/changepassword/',
		views.change_password,
		name='change_password',
	),
	]
