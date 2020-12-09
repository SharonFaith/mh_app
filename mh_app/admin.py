from django.contrib import admin
from .models import User, MhProProfile, UserProfile

# Register your models here.
admin.site.register(User)
admin.site.register(MhProProfile)
admin.site.register(UserProfile)