from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
#from django.contrib.auth.forms import UserChangeForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from clubportal.forms import CreateStaffForm
from clubportal.models import Staff
from starthere.models import Professional
from wodproj.settings import MEDIA_URL
from .forms import (
	EditProfileForm, EditAdditionsForm, CreateProfessionalForm, EditAthleteForm,
	EditGoals, EditPersonRecords,
	)
from .models import AthleteGoal, PersonalRecord

def index(request):
	title = 'AthletePage'
	if hasattr(request.user, 'professional'):
		pro = True
		createpro = False
	elif (request.user.useraddition.user_type == 'pro'
		and not hasattr(request.user, 'professional')):
		pro = False
		createpro = True
	else:
		pro = False
		createpro = False
	#if you have a staff member
	args = {
		'pagetitle': title,
		'professional': pro,
		'createpro': createpro,
	}
	return render(request, 'athportal/ath_home.html', args)# Create your views here.

def view_profile(request):
	#add goals to profile.html
	#maybe prs too
	goals = get_object_or_404(AthleteGoal, athlete=request.user.athlete, active=True)
	all_records = PersonalRecord.objects.all().filter(active=True)
	prs = all_records.filter(athlete=request.user.athlete)
	args = {
		'user': request.user,
		'additions': request.user.useraddition,
		'athlete': request.user.athlete,
		'goals': goals,
		'personalrecords': prs,
		'MEDIA_URL': MEDIA_URL,
	}
	return render(request, 'athportal/profile.html', args)

def edit_athlete_goals(request):
	if request.GET:
		goals_form = EditGoals(request.GET, instance=request.user.athlete)
		if goals_form.is_valid():
			goals_form.save()
			return redirect(reverse('athportal:view_goals'))
		else:
			args = {
				'form': goals_form,
				'issue': 'We had an issue handling your edit request. Please try again.'
			}
			return render(request, 'athportal/edit_goals.html', args)
	else:
		athlete = request.user.athlete
		goals = get_object_or_404(AthleteGoal, athlete=athlete)
		goals_form = EditGoals(instance=goals)
		args = {
			'form': goals_form,
		}
		return render(request, 'athportal/edit_goals.html', args)

def edit_personal_record(request, movement_name):
	if request.method=="POST":
		edit_form = EditPersonRecords(request.POST, instance=request.user.athlete)

		if edit_form.is_valid():
			mvtuid = request.POST['movement'].value()
			if Records.objects.get(
				athlete= request.user.athlete,
				movement=mvtuid,
				active=True,
				).exists():
				#this is to get old personal record
				record = Records.objects.get(
					athlete= request.user.athlete,
					movement=mvtuid,
					active=True,
					)
				if record.record == request.POST['record'].value():
					#means recorded needs editing
					record.measure= request.POST['measure'].value()
					record.date= request.POST['date'].value()
					record.distance_measure= request.POST['distance_measure'].value()
					record.distance= request.POST['distance'].value()
					record.save(
						update_fields=[
							'measure',
							'date',
							'distance',
							'distance_measure'],
					)
					return redirect(reverse('athportal:view_profile'))
				#otherwise need to inactivate old record and save new one
				record.active=False
				record.save()
				edit_form.save()
				return redirect(reverse('athportal:view_profile'))
		else:
			mvtuid = request.POST['movement'].value()
			movement = get_object_or_404(Movement, pk=mvtuid)
			args = {
				'form':edit_form,
				'movement':movement.name
			}
			return render(request, 'athportal/edit_personal_record.html', args)
	else:
		record = get_object_or_404(
			PersonalRecord,
			movement_name=movement_name,
			athlete= request.user.athlete,
			active=True,
		)
		edit_form = EditPersonRecords(instance=record)
		args = {
			'form':edit_form,
		}
		return render(request, 'athportal/edit_personal_record.html', args)


def create_wod(request):
	#how to keep track of free wod gens
	#in athlete model? date of last gen?
	if request.GET:
		settings = WodGenSettings(request.GET)
		if settings.is_valid():
			#wod gen logic
			args ={}
			return render(request, 'athportal/new_generated_wod.html', args)

		form = WodGenSettings()
		args = {
			'error': 'something went wrong',
			'form': form,
		}
		return render(request, 'athportal/set_wod_gen_settings.html', args)
	else:
		athlete = request.user.athlete
		form = WodGenSettings()#need initial values from athlete settings
		args = {'form', form}
		return render(request, 'athportal/set_wod_gen_settings.html', args)

def edit_profile(request):
	if request.method == 'POST':
		account_form = EditProfileForm(request.POST, instance=request.user)
		additions_form = EditAdditionsForm(request.POST,
			request.FILES or None,
			instance=request.user.useraddition,
		)
		athlete_form = EditAthleteForm(request.POST, instance=request.user)

		if account_form.is_valid() and additions_form.is_valid() and additions_form.is_valid():
			account_form.save()
			additions_form.save()
			athlete_form.save()
			return redirect(reverse('athportal:view_profile'))

	else:
		account_form = EditProfileForm(instance=request.user)
		additions_form= EditAdditionsForm(instance=request.user.useraddition)
		athlete_form= EditAthleteForm(instance=request.user.athlete)
		args = {
			'account_form': account_form,
			'additions_form': additions_form,
			'athlete_form': athlete_form,
		}
		return render(request, 'athportal/edit_profile.html', args)

def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)

		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect(reverse('athportal:edit_profile'))
		else:
			return redirect(reverse('athportal:change_password'))

	else:
		form = PasswordChangeForm(user=request.user)
		args = {'form': form}
		return render(request, 'athportal/change_password.html', args)

def login_redirect(request):
	return redirect(reverse('starthere:login'))

def professional_registration(request):
	if request.method == 'POST':
		prof = Professional(user = request.user)
		form = CreateProfessionalForm(request.POST, instance=prof)
		if form.is_valid():
			form.save()
			return redirect(reverse('proportal:pro_home'))
		else:
			pro_form = CreateProfessionalForm()
			args = {
				'pro_form': pro_form,
			}
			return render(request, 'athportal/create_professional_profile.html', args)
	else:
		pro_form = CreateProfessionalForm()
		args = {
			'pro_form': pro_form,
		}
		return render(request, 'athportal/create_professional_profile.html', args)
