from django.utils.crypto import get_random_string
from django.utils.text import slugify
from .models import (
    Athlete, Cycle, MesoCycle, MiniCycle, Wod, Workout, AthleteGoal,
    )

def create_goals(sender, instance, created, **kwargs):
    if created:
        goal = AthleteGoal.objects.create(athlete = instance.athlete)
        goal.save()

# def create_wod(sender, instance, created, **kwargs):
#     if created:
#         slug = make_slug(UserAddition, instance.username)
#         Wod.objects.create(user=instance, slug=slug)
#         Athlete.objects.create(user=instance)
#
# def create_workout(sender, instance, created, **kwargs):
#     if created:
#         slug = make_slug(workout, instance.username)
#         Workout.objects.create(user=instance, slug=slug)
#         Athlete.objects.create(user=instance)
#
# def save_workout(sender, instance, **kwargs):
#     instance.workout.save()
# def save_wod(sender, instance, **kwargs):
#     instance.wod.save()
#
# def make_slug(obj, part1):
#     randstr = get_random_string()
#     slug = slugify("{0}{1}".format(part1, randstr))
#     sl_exist = obj.objects.filter(slug=slug).exists()
#     while sl_exist:
#         randstr = get_random_string()
#         slug = slugify("{0}{1}".format(part1, randstr))
#         sl_exist = obj.objects.filter(slug=slug).exists()
#     return slug
