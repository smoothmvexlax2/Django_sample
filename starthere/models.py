from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/profile_pic/{1}'.format(
        instance.slug,
        filename,
        )

class UserAddition(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
    )

    ACCOUNT_CHOICES=(
        ('f', 'free'),
        ('p', 'premium'),
        ('c', 'club'),
    )

    account_type = models.CharField(
		max_length=1,
		choices=ACCOUNT_CHOICES,
		default='f',
	)
    USER_CHOICES=(
        ('ath', 'Athlete'),
        ('pro', 'Professional'),
    )

    user_type = models.CharField(
        max_length=3,
        choices=USER_CHOICES,
        default='ath',
    )
    image_height = models.PositiveIntegerField(default=200)
    image_width = models.PositiveIntegerField(default=200)
    user_pic = models.ImageField(
        upload_to=user_directory_path,
        height_field='image_height',
        width_field='image_width',
        null=True,
        blank=True,
    )
    start_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "user{0}_id{1}".format(self.user, self.id)

    def save(self, *args, **kwargs):
        if not self.user:
            super(UserAddition, self).save(*args, **kwargs)
        if not self.slug:
            randstr = get_random_string()
            slug = slugify("{0}{1}".format(self.user.username, randstr))
            check = self.__class__
            sl_exist = check.objects.filter(slug=slug).exists()
            while sl_exist:
                randstr = get_random_string()
                slug = slugify("{0}{1}".format(self.user.username, randstr))
                check = self.__class__
                sl_exist = check.objects.filter(slug=slug).exists()
            self.slug = slug
            super(UserAddition, self).save(*args, **kwargs)
        else:
            super(UserAddition, self).save(*args, **kwargs)

@receiver(post_save, sender=User)
def add_user_addition(sender, instance, created, **kwargs):
    if created:
        UserAddition.objects.create(user=instance)
    instance.useraddition.save()

class Professional(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
    )
    company = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    bio = models.TextField(
        max_length=191,
        blank=True,
        null=True,
    )
    specialty = models.CharField(
        max_length=191,
        blank=True,
        null=True,
    )
    credentials = models.TextField(
        default="none",
        blank=True,
        null=True,
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return "user{0}_id{1}".format(self.user, self.id)

class Athlete(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    GENDER_CHOICES=(
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Other', 'Other'),
    )
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
    )
    weight = models.IntegerField(default=100)
    UNIT_CHOICES=(
        ('lbs', 'lbs'),
        ('kgs', 'kgs'),
    )
    weight_units = models.CharField(
        max_length=3,
        choices=UNIT_CHOICES,
        default='lbs',
    )
    time_per_day = models.IntegerField(default=50)
    active = models.BooleanField(default=True)
    days_per_week = models.IntegerField(default=5)
    strength_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    stamina_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    capacity_score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "user{0}_id{1}".format(self.user, self.id)

@receiver(post_save, sender=User)
def create_athlete(sender, instance, created, **kwargs):
    if created:
        Athlete.objects.create(user=instance)
    instance.athlete.save()
