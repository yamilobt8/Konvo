from django.contrib import admin
from a_users.models import Profile, PasswordHistory

# Register your models here.
admin.site.register(Profile)
admin.site.register(PasswordHistory)