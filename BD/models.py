from django.db import models



# Create your models here.
class AddBD(models.Model):
    add_BD_email = models.EmailField(max_length=60)
    add_BD_username = models.CharField(max_length=100)
    add_BD_password = models.CharField(max_length=100)

    def __str__(self):
        return self.add_bd_username
class BDLogin(models.Model):
    BD_login_username = models.CharField(max_length=100)
    BD_login_password = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

