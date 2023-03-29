from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "username"}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "password"}))