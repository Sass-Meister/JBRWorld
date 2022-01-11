from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30, primary_key=True)
    email = models.CharField(max_length=20) # Necessary?
    anon = models.BooleanField()

# What do these fields mean?
# https://developer.spotify.com/documentation/general/guides/authorization-guide/
# The char lengths are from testing not from official documentation so if they change this will be messed up
class AuthSet(models.Model):
    code = models.CharField(max_length=398)
    access_token = models.CharField(max_length=178, primary_key=True)
    refresh_token = models.CharField(max_length=131)
    expires_at = models.DateTimeField()

class Party(models.Model):
    authset = models.OneToOneField(AuthSet, on_delete=models.DO_NOTHING)
    code = models.IntegerField(primary_key=True)
#    users = models.ManyToManyField(User, related_name='+')
#    host = models.OneToOneField(User, on_delete=models.PROTECT)

