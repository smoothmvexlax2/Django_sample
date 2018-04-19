from string import capwords
from random import randint
from django.db import models
from starthere.models import Athlete
from django.utils import timezone
from django.utils.text import slugify

def equipment_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'equipment_{0}/image_{1}/{2}'.format(
        instance.equipment.slug,
        instance.equipment.name,
        filename,
        )
def workout_directory_path(instance, filename):
    #-----------------------------------
    #need to add the part for username**
    #-----------------------------------
    return 'user_{0}/wodvideos/%Y/%m/%d/workout/{1}{2}'.format(
        username,
        instance.workout.slug,
        filename,
        )

class Cycle(models.Model):
    athlete = models.ForeignKey(
        Athlete,
        on_delete=models.CASCADE,
    )
    active = models.BooleanField(default=True)

class MesoCycle(models.Model):
    cycle = models.ForeignKey(
        Cycle,
        on_delete=models.CASCADE,
    )
    number_of_weeks = models.IntegerField(default=6)
    time_per_day = models.IntegerField(default=60)
    days_off = models.CharField(max_length=191)
    #days_off will be a list of the names of each days_off
    active = models.BooleanField(default=True)
    load_volume = models.IntegerField(default=0)
    rep_volume = models.IntegerField(default=0)
    total_push = models.IntegerField(default=0)
    total_pull = models.IntegerField(default=0)

class MiniCycle(models.Model):
    mesocycle = models.ForeignKey(
        MesoCycle,
        on_delete=models.CASCADE,
    )
    start_date = models.DateField()
    load_volume = models.IntegerField(default=0)
    rep_volume = models.IntegerField(default=0)
    total_up_push = models.IntegerField(default=0)
    total_up_pull = models.IntegerField(default=0)
    total_low_push = models.IntegerField(default=0)
    total_low_pull = models.IntegerField(default=0)
    current = models.BooleanField(default=False)
    sunday = models.IntegerField(default=0)
    monday = models.IntegerField(default=0)
    tuesday = models.IntegerField(default=0)
    wednesday = models.IntegerField(default=0)
    thursday = models.IntegerField(default=0)
    friday = models.IntegerField(default=0)
    saturday = models.IntegerField(default=0)

class Wod(models.Model):
    minicycle = models.ForeignKey(
        MiniCycle,
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
    )
    load_volume = models.IntegerField(default=0)
    rep_volume = models.IntegerField(default=0)
    total_up_push = models.IntegerField(default=0)
    total_up_pull = models.IntegerField(default=0)
    total_low_push = models.IntegerField(default=0)
    total_low_pull = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "mini{0}<id>{1}".format(self.minicycle, self.id)

class Workout(models.Model):
    wod = models.ForeignKey(
        Wod,
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
    )
    rounds = models.IntegerField(default=0)
    sets = models.IntegerField(default=0)
    reps = models.CharField(max_length=191)
    loads = models.CharField(max_length=191)
    intervals = models.IntegerField(default=0)
    rest_per_interval = models.IntegerField(default=0)
    scheme = models.IntegerField(default=0)
    estimated_time = models.IntegerField(default=0)
    score = models.IntegerField(default=-1)
    #for score if negative then time in secs, otherwise reps
    movements = models.CharField(max_length=191)
    video = video = models.FileField(
        upload_to=workout_directory_path,
        default="",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=30)
    athlete_comments = models.TextField(
        default="",
        blank=True,
        null=True,
        )
    details = models.CharField(max_length=255)

    def __str__(self):
        return "wod{0}<id>{1}".format(self.wod, self.id)

class WoStyle(models.Model):
    name = models.CharField(
		max_length=30,
		default='general',
	)

    def __str__(self):
        return "{}".format(capwords(self.name))

class Method(models.Model):
    name = models.CharField(
		max_length=20,
		default='general strength',
	)
    def __str__(self):
        return "{0}<id>{1}".format(self.name, self.id)

class MovementType(models.Model):
    MOVEMENT_TYPE_CHOICES = (
        ('Sports Conditioning', 'Sports Conditioning'),
        ('Lifting', 'Lifting'),
        ('Gymnastics', 'Gymnastics'),
    )
    name = models.CharField(
        max_length=30,
        choices=MOVEMENT_TYPE_CHOICES,
    )

    def __str__(self):
        return "{0}<id>{1}".format(self.name, self.id)

class MovementTypeCategory(models.Model):
    name = models.CharField(max_length=30)
    movement_type = models.ForeignKey(
        MovementType,
        on_delete=models.CASCADE,
    )
    class Meta:
        verbose_name_plural = "movement type categories"

    def __str__(self):
        return "{}".format(self.name)

class Gym(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(capwords(self.name))

class Equipment(models.Model):
    name = models.CharField(max_length=50)
    equipment_type = models.CharField(max_length=30)
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,
    )
    image_height = models.PositiveIntegerField(default=400)
    image_width = models.PositiveIntegerField(default=400)
    picture = models.ImageField(
        upload_to=equipment_directory_path,
        height_field='image_height',
        width_field='image_width',
        default="",
        blank=True,
        null=True,
    )
    class Meta:
        verbose_name_plural = "equipment"

    def __str__(self):
        return "{0}{1}".format(self.name, self.id)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify("{0}{1}".format(self.name, randint(100,10000)))
            check = self.__class__
            sl_exist = check.objects.filter(slug=slug).exists()
            while sl_exist:
                randstr = get_random_string(length=4)
                slug = slugify("{0}{1}".format(self.name, randint(100,10000)))
                check = self.__class__
                sl_exist = check.objects.filter(slug=slug).exists()
            self.slug = slug
            super(Equipment, self).save(*args, **kwargs)
        else:
            super(Equipment, self).save(*args, **kwargs)

class Movement(models.Model):
    name = models.CharField(max_length=50)
    equipment_list = models.CharField(max_length=255)
    seconds_per_rep = models.IntegerField(default=3)
    pushpull = models.IntegerField(default=10000)
    #dumby,upper body push, upper body pull, lower body push, lower body pushpull
    #ex: 10110
    plane = models.CharField(max_length=3)
    #x is horizontal(left and right), y is vertical, z is forward or back
    #ex lateral long is x and bench press is z
    details = models.TextField()
    movement_type = models.ForeignKey(
        MovementType,
        on_delete=models.CASCADE,
    )
    movement_type_category = models.ForeignKey(
        MovementTypeCategory,
        on_delete=models.CASCADE,
    )
#    video = EmbedVideoField()
    def __str__(self):
        return "{0}".format(capwords(self.name))

class MainLift(models.Model):
    name =  models.CharField(max_length=50)

    def __str__(self):
        return "{0}<id>{1}".format(self.name, self.id)

class MainLiftGroup(models.Model):
    movement = models.ForeignKey(
        Movement,
        on_delete=models.CASCADE,
    )
    mainlift = models.ForeignKey(
        MainLift,
        on_delete=models.CASCADE,
    )

class CoreLift(models.Model):
    mainlift = models.ForeignKey(
        MainLift,
        on_delete=models.CASCADE,
    )
    wostyle = models.ForeignKey(
        WoStyle,
        on_delete=models.CASCADE,
    )

class AthleteGoal(models.Model):
    athlete = models.ForeignKey(
        Athlete,
        on_delete=models.CASCADE,
    )
    strength = models.BooleanField(default=False)
    lose_weight = models.BooleanField(default=False)
    gain_muscle = models.BooleanField(default=False)
    gpp = models.BooleanField(default=True)
    skills = models.CharField(max_length=191, blank=True, null=True)
    #will be a list of max 3 movement_ids
    active = models.BooleanField(default=True)

class PersonalRecord(models.Model):
    RECORD_MEASURE_CHOICES = (
        ('lbs', 'Lbs'),
        ('kgs', 'Kgs'),
        ('time', 'Time'),
    )
    DISTANCE_MEASURE_CHOICES = (
        ('m', 'Meters'),
        ('km', 'Kilometers'),
        ('miles', 'Miles'),
        ('yds', 'Yards'),
        ('ft', 'Feet'),
        ('', ''),
    )
    record = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        #allows up to 99,999.99
        #ten hours = 36000 secs
        #either weight or secs
    )
    measure = models.CharField(
        max_length=30,
        choices=RECORD_MEASURE_CHOICES,
        default='lbs',
    )
    distance = models.DecimalField(
        default=0.00,
        max_digits=7,
        decimal_places=2,
    )
    distance_measure = models.CharField(
        max_length=30,
        choices=DISTANCE_MEASURE_CHOICES,
        default='',
        null=True,
        blank=True,
    )
    date = models.DateField(default= timezone.now)
    active = models.BooleanField(default=True)
    athlete = models.ForeignKey(
        Athlete,
        on_delete=models.CASCADE,
    )
    movement_name = models.CharField(
        max_length=50,
        default='',
        null=True,
        blank=True,
    )
    movement = models.ForeignKey(
        Movement,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return "{0}_{1}".format(self.athlete, self.movement)

    def save(self, *args, **kwargs):
        if Movement.objects.filter(id = self.movement_id).exists():
            mvt = Movement.objects.get(id=self.movement_id)
            name = mvt.name
            self.movement_name = name
            super(PersonalRecord, self).save(*args, **kwargs)
        else:
            super(PersonalRecord, self).save(*args, **kwargs)

class MovementScale(models.Model):
    scale_1 = models.IntegerField(default=0)
    scale_2 = models.IntegerField(default=0)
    scale_3 = models.IntegerField(default=0)
    movement = models.ForeignKey(
        Movement,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "scale for {0}".format(self.movement)

class GymLocation(models.Model):
    street_address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.IntegerField(default=0)
    country = models.CharField(max_length=50)
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return "gym{0}_loc{1}".format(self.gym, self.id)

class GymEquipment(models.Model):
    gym_location = models.ForeignKey(
        GymLocation,
        on_delete=models.CASCADE,
    )
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE
    )
    confidence = models.DecimalField(
        default=0.50,
        max_digits=3,
        decimal_places=2,
    )
    number_of_verifications = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    location_verified = models.BooleanField(default=False)

class HeavyLiftTable(models.Model):
    mainlift = models.ForeignKey(
        MainLift,
        on_delete=models.CASCADE,
    )
    GENDER_CHOICES = (
        ("Female", "Female"),
        ("Male", "Male"),
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )
    body_weight = models.IntegerField()
    untrained = models.IntegerField()
    novice = models.IntegerField()
    intermediate = models.IntegerField()
    advanced = models.IntegerField()
    elite = models.IntegerField()
