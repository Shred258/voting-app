from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Poll, Choice, Vote

admin.site.register(CustomUser)
admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote)