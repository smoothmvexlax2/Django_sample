from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms.widgets import NumberInput
from django.utils.translation import gettext_lazy as gt_
from .models import UserAddition, Athlete
#inherite from UserCreationForm

class CreateAccountForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super(CreateAccountForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class UserAdditionForm(forms.ModelForm):
    class Meta:
        #user_type needs to exclude staff option
        model = UserAddition
        fields = (
            'user_type',
            'user_pic',
        )
        labels = {
            'idfrom_employer': gt_("Employee ID/#"),
            'date_of_birth': gt_("Date of Birth (Day, Month, Year)"),
        }

class CreateAthleteForm(forms.ModelForm):
    days_per_week = forms.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(7)],
        )
    class Meta:
        model = Athlete
        fields = (
            'gender',
            'weight',
            'weight_units',
            'time_per_day',
            'days_per_week',
        )
