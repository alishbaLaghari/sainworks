from django import forms
from .models import EmployeeLogin

class EmployeeProfileUpdateForm (forms.ModelForm):
    new_profile_picture = forms.ImageField(label='New Profile Picture', required=False)

    class Meta:
        model = EmployeeLogin
        fields = ['profile_picture', 'new_profile_picture', 'age', 'bio']
        
        
        
        