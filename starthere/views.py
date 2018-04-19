from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from wodproj.email_info import EMAIL_HOST_USER
from .activatecode import account_activation_token
from .forms import CreateAccountForm, UserAdditionForm, CreateAthleteForm


def index(request):
	title = 'Home'
	args = {'pagetitle': title}
	return render(request, 'starthere/home.html', args)

def account_activation_sent(request):
	title = 'Emailsent'
	args = {'pagetitle': title}
	return render(request, 'newaccount/activation_email_done.html', args)

def account_activate(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user= None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return render(request, 'newaccount/account_confirmation_complete.html')

	else:
		return render(request, 'newaccount/account_activation_invalid.html')

def login_redirect(request):
	return redirect(reverse('starthere:login'))

def register(request):
	if request.method =='POST':
		account_form = CreateAccountForm(request.POST)
		additions_form = UserAdditionForm(request.POST,
			request.FILES or None,
			)
		athlete_form = CreateAthleteForm(request.POST)

		if account_form.is_valid() and additions_form.is_valid() and athlete_form.is_valid():
			user = account_form.save(commit=False)
			user.is_active = False
			user.save()

			newuser = get_object_or_404(User, email=user.email)
			additions_form = UserAdditionForm(request.POST,
				request.FILES or None,
				instance = newuser,
				)
			additions_form.save()

			athlete_form = athlete_form = CreateAthleteForm(request.POST, instance=newuser)
			athlete_form.save()

			current_site = get_current_site(request)
			subject = 'Activate WodProj Account'
			message = render_to_string('newaccount/activate_account_email.html', {
				'user': user,
				'domain': current_site,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token': account_activation_token.make_token(user),
			})
			#uid needs to be protected so need extra field in user model
			#and need to to not use user.pk
			send_mail(
				subject,
				message,
				EMAIL_HOST_USER,
				[user.email],
			)

			return redirect(reverse('starthere:activation_sent'))
		else:
			account_form = CreateAccountForm()
			additions_form = additions_form
			athlete_form = athlete_form
			args = {
				'account_form': account_form,
				'additions_form': additions_form,
				'athlete_form': athlete_form,
			}
			return render(request, 'starthere/reg_form.html', args)
	else:
		account_form = CreateAccountForm()
		additions_form = UserAdditionForm()
		athlete_form = CreateAthleteForm()
		args = {
			'account_form': account_form,
			'additions_form': additions_form,
			'athlete_form': athlete_form,
		}
		return render(request, 'starthere/reg_form.html', args)
