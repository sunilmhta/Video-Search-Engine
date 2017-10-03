from django import forms

class initialSearch(forms.Form):
   search_key_text = forms.CharField(max_length = 100)
   #password = forms.CharField(widget = forms.PasswordInput())
class userLogin(forms.Form):
	username = forms.CharField(max_length = 100)
	password = forms.CharField(max_length=100)


class userRegistration(forms.Form):
	first_name=forms.CharField(max_length=100)
	last_name=forms.CharField(max_length=100)
	# email=forms.EmailField()
	# email=forms.EmailField()
	# sex=forms.CharField(max_length=10)
	# age=forms.IntField()
	# password=forms.CharField(max_length=100)

