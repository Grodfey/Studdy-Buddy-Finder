from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import UserBio
from django import forms


class ChangeProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'}))
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'size': '20'}))
    password = None
    #password = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

class ChangeBioForm(forms.ModelForm):
    degree = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'}))
    year = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'}))
    bio = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control', 'size': '20'}))
    class Meta:
        model = UserBio
        fields = ['degree', 'year', 'bio']