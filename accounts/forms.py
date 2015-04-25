from django import forms
from django.contrib.auth.models import User



class UserLoginForm(forms.Form):
    username = forms.CharField( label="Username", max_length=20 )
    password = forms.CharField( label="Password", 
                                widget=forms.PasswordInput() )


class UserRegisterForm(forms.ModelForm):
    # rewrite default variables (User)
    username = forms.CharField( label="Username", max_length=20 ) 
    password = forms.CharField( label="Password", 
                                widget=forms.PasswordInput() )

    class Meta:
        model = User
        fields = ( 'username', 'email', 'password' )
    
