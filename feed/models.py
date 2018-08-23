from django.db import models
from django.utils import timezone
from datetime import datetime,timedelta, time
from django.contrib.auth.models import User


def get_next_weekday(startdate, weekday):
    """
    @startdate: given date, in format '2013-05-25'
    @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
    """
    d = datetime.strptime(startdate, '%Y-%m-%d')
    t = timedelta((7 + weekday - d.weekday()) % 7)
    return (d + t).strftime('%Y-%m-%d')


class Course(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=4000, blank=True, null=True)
    location = models.CharField(max_length=50, blank=False, null=False)
    par = models.IntegerField(blank=False, null=False)
    yardage = models.CharField(blank=False, null=False, max_length=140)
    img = models.CharField(blank=True, null=True, max_length=50)


    def __str__(self):
        return "{} - {}".format(self.name, self.location)


class Dogfight(models.Model):

    date = models.DateField(default=get_next_weekday(timezone.now().strftime('%Y-%m-%d'), 5), blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False, default=time(hour=7, minute=30))
    number_of_groups = models.IntegerField(blank=False, null=False, default=5)
    course = models.ForeignKey(Course, related_name='dogfight_course', on_delete=models.CASCADE)


    def __str__(self):
        return "Dogfight on {} | {} @ {} for {} groups".format(self.course.name, self.date, self.start_time, self.number_of_groups)

    def formal_text(self):
        return "The Current Dogfight is at {} on {}. There are {} Tee Times starting at {}. <br /><br /><small>Below is the players currently signed up.</small>".format(self.course.name, self.date, self.number_of_groups, self.start_time)




# TODO: Create Current Player Model, include Waiting List based off of number_of_groups
class DogfightList(models.Model):
    dogfight = models.ForeignKey(Dogfight, related_name='dogfight', on_delete=models.CASCADE)
    golfer = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    waiting = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return "{}, {} | {} at {} | Waiting: {}".format(self.golfer.last_name, self.golfer.first_name, self.dogfight.date, self.dogfight.course, self.waiting)