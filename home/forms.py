from django import forms
from home.models import registered_as
class regisForm(forms.Form):
	regis_mob=forms.IntegerField()
	regis_pass=forms.CharField(max_length=20)
	widgets={
		 		'regis_pass': forms.PasswordInput(),
		}
	def clean(self):
		super(regisForm,self).clean()
		password = self.cleaned_data.get('regis_pass')
		mobile = self.cleaned_data.get('regis_mob')
		if len(str(mobile))<10:
			self._errors['regis_mob'] =self.error_class(['Incorrect Number Formate'])
		if len(password)<5:
			self._errors['regis_pass'] =self.error_class(['Mininmum 5 character'])
		return self.cleaned_data

class getForm(forms.Form):
	your_otp=forms.CharField(max_length=6)

class loginForm(forms.Form):
	login_mob=forms.IntegerField()
	login_pass=forms.CharField(max_length=20)

	def clean(self):
		super(loginForm,self).clean()
		password = self.cleaned_data.get('login_pass')
		mobile = self.cleaned_data.get('login_mob')
		if len(str(mobile))<10 or len(str(mobile))>10:
			self._errors['login_mob'] =self.error_class(['Incorrect Number Formate'])
		if len(password)<5:
			self._errors['login_pass'] =self.error_class(['Mininmum 5 character'])
			return self.cleaned_data

class cartForm(forms.Form):
	CHOICES=[('select1','select 1'),('select2','select 2'),('sharad','mehra')]
	like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class imgForm(forms.Form):
	img=forms.FileField()
	def __init__(self, *args, **kwargs):
		super(imgForm, self).__init__(*args, **kwargs)
		self.fields['img'].widget =forms.FileInput(attrs={
            'id': 'imgupload',
            'style':'display:none',
            'onchange':'loadFile(event)'})
		