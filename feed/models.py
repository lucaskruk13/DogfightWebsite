from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=4000, blank=True, null=True)
    location = models.CharField(max_length=50, blank=False, null=False)
    par = models.IntegerField(blank=False, null=False)
    yardage = models.CharField(blank=False, null=False, max_length=140)
    img = models.CharField(blank=True, null=True, max_length=50)


    def __str__(self):
        return "{} - {}".format(self.name, self.location)