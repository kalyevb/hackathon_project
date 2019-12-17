from django.contrib import admin
from .models import *
from django.contrib.auth.models import User


admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
