from django.forms import ModelForm 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import CarImage, UserProfile,Comment



class CreateRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name','last_name')

class Login(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())


class ImageForm(ModelForm):
    class Meta:
        model = CarImage
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class PasswordResetForm(forms.Form):
        error_messages ={'password mismatch':('The two passwords didnot match ..')} 
        password1=forms.CharField(widget=forms.PasswordInput,label="New password",required=True)
        password2=forms.CharField(widget=forms.PasswordInput,required=True,label="New Password Confirmation")


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']

class CommentForm(forms.ModelForm):
    class Meta:
        model =Comment
        fields=('content',)        