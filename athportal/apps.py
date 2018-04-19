from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Wod, Workout, Athlete
from .signals import create_goals, #create_wod, save_workout


class AthportalConfig(AppConfig):
    name = 'athportal'

    def ready(self):
        post_save.connect(create_goals, sender=Athlete)
    #     post_save.connect(create_wod, sender=Wod)
    #     post_save.connect(save_Workout, sender=Workout)
