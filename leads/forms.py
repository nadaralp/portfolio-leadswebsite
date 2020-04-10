from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())