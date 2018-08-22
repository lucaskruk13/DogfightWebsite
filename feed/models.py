from django.db import models
from django.utils import timezone

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
    date = models.DateField(default=timezone.now, blank=False, null=False)
    start_time = models.TimeField(default=timezone.now, blank=False, null=False)
    number_of_groups = models.IntegerField(blank=False, null=False)
    course = models.ForeignKey(Course, related_name='dogfight_course', on_delete=models.CASCADE)


    def __str__(self):
        return "Dogfight on {} | {} @ {} for {} groups".format(self.course.name, self.date, self.start_time, self.number_of_groups)

    def formal_text(self):
        return "The Current Dogfight is at {} on {}. There are {} Tee Times starting at {}. <br /><br /><small>Below is the players currently signed up.</small>".format(self.course.name, self.date, self.number_of_groups, self.start_time)