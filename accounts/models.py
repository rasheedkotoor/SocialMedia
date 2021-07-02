from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save


# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=150, blank=True, null=True, unique=True)
    is_verified = models.BooleanField(default=False)
    is_union = models.BooleanField(default=False)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self):
        return reverse('student:details', args=[self.pk])


class Union(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True, null=True)
    reg_num = models.CharField(max_length=20, blank=True, null=True, unique=True)
    est_date = models.DateField(null=True, blank=True)
    background_img = models.ImageField(upload_to='bg_pic/', height_field=None, width_field=None, null=True)
    logo = models.ImageField(upload_to='union_logo/', height_field=None, width_field=None, null=True)
    college_name = models.CharField(max_length=150, blank=True, null=True)
    college_short_name = models.CharField(max_length=30, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    college_est_date = models.DateField(null=True, blank=True)
    college_logo = models.ImageField(upload_to='collage_logo/', height_field=None, width_field=None, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # set when created

    def __str__(self):
        return str(self.user)


GENDER = (('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'))


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='Male', null=True, blank=True)
    admission_num = models.BigIntegerField(blank=True, null=True, unique=True)
    batch = models.CharField(max_length=200, blank=True, null=True)
    batch_num = models.BigIntegerField(blank=True, null=True, unique=True)
    union = models.ForeignKey(Union, on_delete=models.CASCADE, blank=True, null=True)
    membership_num = models.CharField(max_length=20, blank=True, null=True, unique=True)
    membership_img = models.ImageField(upload_to='memb_pic/', height_field=None, width_field=None, blank=True,
                                       null=True)
    profile_img = models.ImageField(upload_to='profile_pic/', height_field=None, width_field=None, blank=True,
                                    null=True)
    background_img = models.ImageField(upload_to='background_pic/', height_field=None, width_field=None, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # set when created
    # general info
    hobbies = models.TextField(blank=True, null=True)
    interests = ArrayField(models.CharField(max_length=10, default='Arabic', blank=True, null=True), null=True)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Student.objects.create(user=instance)
        except:
            pass
# post_save.connect(post_save_user_model_receiver, sender=User)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_user')
    timestamp = models.DateTimeField(auto_now_add=True)  # set when created

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)


# Explorer, Talker, Admirer, Searcher, Groups and Events


class PointBadges(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userbadge')
    point = models.BigIntegerField(blank=True, null=True)
    badge = ArrayField(models.CharField(max_length=10, default="starter", blank=True, null=True), null=True)


class MemberRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='from_member')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to_member')
    timestamp = models.DateTimeField(auto_now_add=True)  # set when created

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)


class PageAdmin(models.Model):
    page = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='page')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin')
    timestamp = models.DateTimeField(auto_now_add=True)  # set when created
