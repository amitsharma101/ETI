from django import forms
from .models import extendeduser

class ProfileForm(forms.ModelForm):
	class Meta:
		model = extendeduser
		fields = ['semester','phone_num']