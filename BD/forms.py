from django import forms
from .models import BDLogin

class BDProfileUpdateForm(forms.ModelForm):
    new_profile_picture = forms.ImageField(label='New Profile Picture', required=False)

    class Meta:
        model = BDLogin
        fields = ['profile_picture', 'new_profile_picture', 'age', 'bio']
        