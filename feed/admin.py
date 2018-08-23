from django.contrib import admin
from .models import Course, Dogfight, DogfightPlayer

class DogfightPlayerTabular(admin.TabularInline):
    model = DogfightPlayer
    extra = 1

class DogfightAdmin(admin.ModelAdmin):
    inlines = [DogfightPlayerTabular]




admin.site.register(Course)
admin.site.register(Dogfight, DogfightAdmin)

