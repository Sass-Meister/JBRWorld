from django.contrib import admin
from .models import User, AuthSet, Party

# Register your models here.
admin.site.register(User)
admin.site.register(Party)
admin.site.register(AuthSet)
