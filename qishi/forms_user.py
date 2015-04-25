from django import forms
from django.contrib.auth.models import User



class UserLoginForm(forms.Form):
    username = forms.CharField( 
        label="Username", max_length=20,
        widget=forms.TextInput(attrs={
            'id':          'loginUsername',
            'placeholder': 'Username',
            'class':       'form-control',
            'required':    '',
            'autofocus':   '',
            'type':        'text'
        }))

    password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput({
            'id':          'loginPassword',
            'placeholder': 'Password',
            'class':       'form-control',
            'required':    '',
            'type':        'password'
        }))


class UserRegisterForm(forms.ModelForm):
    # rewrite default variables (User)
    username = forms.CharField( 
        label="Username", max_length=20,
        widget=forms.TextInput(attrs={
            'id':          'registerUsername',
            'placeholder': 'Username',
            'class':       'form-control',
            'required':    '',
            'autofocus':   '',
            'type':        'text',
        })) 
    email = forms.CharField( 
        label="Email", max_length=20,
        widget=forms.TextInput(attrs={
            'id':          'registerEmail',
            'placeholder': 'Email address',
            'class':       'form-control',
            'required':    '',
            'autofocus':   '',
            'type':        'email'
        }))
    password = forms.CharField( 
        label="Password", 
        widget=forms.PasswordInput(attrs={
            'id':          'registerPassword',
            'placeholder': 'Password',
            'class':       'form-control',
            'required':    '',
            'type':        'password'
        }))

    class Meta:
        model = User
        fields = ( 'username', 'email', 'password' )
    
