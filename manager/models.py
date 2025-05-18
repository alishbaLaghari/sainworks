from django.db import models
from employee.models import AddEmployee
# Create your models here.
class AddManager(models.Model):
    add_manager_email=models.EmailField(max_length=60)
    add_manager_username = models.CharField(max_length=100)
    add_manager_password = models.CharField(max_length=100)

class ManagerLogin(models.Model):
    manager_login_username = models.CharField(max_length=100)
    manager_login_password = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    

class Project(models.Model):
    project_manager = models.CharField(max_length=255)  # Assuming storing username
    project_name = models.CharField(max_length=255)
    project_type = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    milestones = models.IntegerField()
    description = models.TextField()

      # Return a string representation of the project

class TeamMemberTask(models.Model):
    project = models.ForeignKey(Project, related_name='team_tasks', on_delete=models.CASCADE)
    team_member = models.CharField(max_length=255)
    task_to_be_allotted = models.CharField(max_length=255)
    
class comment(models.Model):
    comment=models.TextField(max_length=400)