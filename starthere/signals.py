from django.utils.crypto import get_random_string
from django.utils.text import slugify
from .models import UserAddition, Athlete

def create_user_additions(sender, instance, created, **kwargs):
    if created:
        slug = make_slug(UserAddition, instance.username)
        UserAddition.objects.create(user=instance, slug=slug)
        Athlete.objects.create(user=instance)


def save_user_additions(sender, instance, **kwargs):
    instance.useraddition.save()

def make_slug(obj, part1):
    randstr = get_random_string()
    slug = slugify("{0}{1}".format(part1, randstr))
    sl_exist = obj.objects.filter(slug=slug).exists()
    while sl_exist:
        randstr = get_random_string()
        slug = slugify("{0}{1}".format(part1, randstr))
        sl_exist = obj.objects.filter(slug=slug).exists()
    return slug
