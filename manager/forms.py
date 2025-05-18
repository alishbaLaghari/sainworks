from django import forms
from .models import ManagerLogin

class ManagerProfileUpdateForm(forms.ModelForm):
    new_profile_picture = forms.ImageField(label='New Profile Picture', required=False)

    class Meta:
        model = ManagerLogin
        fields = ['profile_picture', 'new_profile_picture', 'age', 'bio']
# forms.py (if used)

from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_type', 'start_date', 'end_date', 'milestones', 'description']
