from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from .signals import create_user_additions, save_user_additions


class StarthereConfig(AppConfig):
    name = 'starthere'

    def ready(self):
        post_save.connect(create_user_additions, sender=User, dispatch_uid="create_useradd_uid")
        post_save.connect(save_user_additions, sender=User, dispatch_uid="save_useradd_uid")
