from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from django.core.validators import RegexValidator
import re

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    handicap = models.CharField(max_length=6, null=False, blank=False,default=0, validators=[
        RegexValidator(
            regex="^[+]?\d*\.?\d*$",
            message="Invalid Handicap",
            code='invalid_handicap'
        )
    ])
    initial = models.BooleanField(default=True) # Initial Value to update the handicap


    # TODO: write Average & Quota Building Tests Including Failing conditions
    def getCurrentQuota(self):
        avg = Scores.objects.filter(profile=self).order_by('-created_at')[:5].aggregate(Avg('score'))
        if avg['score__avg']:
            return round(avg['score__avg'])

    def getHandicap(self):
        return float(self.handicap)


class Scores(models.Model):
    profile = models.ForeignKey(Profile, related_name='scores', on_delete=models.CASCADE)
    # TODO: Add Course Foreign Key

    score = models.IntegerField(default=0, null=False, blank=False)
    created_at = models.DateField(auto_now_add=True)


def on_profile_save(sender, instance, **kwargs):

    scoresCount = Scores.objects.filter(profile=instance).count()
    handicap = instance.handicap

    # if there are no scores, but the Initial Value is false, let's add the baseline scores
    # The initial value is changed by the view's is form_valid method
    if ((not instance.initial) and (scoresCount == 0)):
        for i in range(5):
            score = Scores()
            score.profile = instance # Instance is of class Profile
            score.score = generateInitialQuota(instance.handicap)
            score.save()


post_save.connect(on_profile_save, sender=Profile) # Links Scores saving function to the function on_profile_save

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def generateInitialQuota(handicap):

    # when we get here, the handicap should be valid
    # if the handicap is + we need to convert it to - to add to 36
    handicap = float(re.sub(r"[+]", "-", handicap))

    return round(36.0 - handicap)





