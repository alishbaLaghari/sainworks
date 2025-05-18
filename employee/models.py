from django.db import models

# Create your models here.
class AddEmployee(models.Model):
    add_employee_email = models.EmailField(max_length=60)
    add_employee_username = models.CharField(max_length=100)
    add_employee_password = models.CharField(max_length=100)

    def __str__(self):
        return self.add_employee_username
class EmployeeLogin(models.Model):
    employee_login_username = models.CharField(max_length=100)
    employee_login_password = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
