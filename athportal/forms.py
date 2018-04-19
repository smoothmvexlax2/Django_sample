from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as gt_
from starthere.models import UserAddition, Professional, Athlete
from . import models
#inherite from UserCreationForm

class WodGenSettings(forms.Form):
    mvtexlcusion1 = forms.IntegerField(required=False)#will be movement pk
    mvtexlcusion2 = forms.IntegerField(required=False)
    duration = forms.IntegerField()#in minutes
    workout_style = forms.IntegerField()#will be wostyle pk
    location = forms.IntegerField()#will be gym_location pk

class EditPersonRecords(forms.ModelForm):
    #need to validate the movement name is a movement
    class Meta:
        model = models.PersonalRecord
        exclude = (
            'athlete',
            'active',
        )

class EditGoals(forms.ModelForm):

    class Meta:
        boolist = (
            (False, 'No'),
            (True, 'Yes'),
        )

        movementobj = models.Movement.objects.all()
        mvtlist = ((mvt.pk, mvt.name) for mvt in movementobj)

        model = models.AthleteGoal
        fields = (
            'strength',
            'lose_weight',
            'gain_muscle',
            'gpp',
            'skills',
            )

        widgets = {
            'strength': forms.Select(choices=boolist),
            'lose_weight': forms.Select(choices=boolist),
            'gain_muscle': forms.Select(choices=boolist),
            'gpp': forms.Select(choices=boolist),
            'skills': forms.SelectMultiple(choices=mvtlist),
        }
        labels = {
            'strength': gt_("Gain Strength"),
            'lose_weight': gt_("Lose Weight"),
            'gain_muscle': gt_("Gain Muscle Mass"),
            'gpp': gt_("Increase General Physical Preparedness"),
            'skills': gt_("Specific Movements You Want To Achieve"),
        }
class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        )
        #exclude = () can be used instead of fields

class EditAdditionsForm(forms.ModelForm):

    class Meta:
        model = UserAddition
        fields = (
            'user_pic',
            'user_type',
        )

class EditAthleteForm(forms.ModelForm):
    days_per_week = forms.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(7)],
        )
    class Meta:
        model = Athlete
        fields = (
            'gender',
            'weight',
            'time_per_day',
            'days_per_week',
        )

class CreateProfessionalForm(forms.ModelForm):

    class Meta:
        model = Professional
        fields = (
            'company',
            'specialty',
            'credentials',
            'bio',
        )
