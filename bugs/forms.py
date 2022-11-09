from django import forms
from .models import Bug,File

from users.models import User

from crispy_forms.helper import FormHelper

class BugUpdateForm(forms.ModelForm):

	class Meta:
		model = Bug
		fields = ['title', 'description']




class addFileForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(addFileForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_show_labels = False 
		self.fields['file'].label = ''
	class Meta:

		model = File
		fields = ['file']
