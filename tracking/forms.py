from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


#Input Product
class InputProduct (forms.ModelForm):
    class Meta:
        model = Product
        fields = ['Varietas', 'Volume', 'HarvestAge', 'HarvestMethod', 'WaterContent']
        labels = {
            'HarvestAge': 'Umur Panen',
            'HarvestMethod': 'Metode Panen',
            'WaterContent' : 'Kadar Air (%)',
            'Volume': 'Volume (Kg)'
        }
        


#Registration

class ProfileUserRegisterForm(UserCreationForm):
    Role = forms.ChoiceField(choices=ProfileUser.ROLE_CHOICES, label ='Pekerjaan')

    class Meta:
        model = ProfileUser
        fields = ['username', 'email', 'Role', 'password1', 'password2']
        labels = {
            'username'  : 'Nama Pengguna',
            'email'     : 'Alamat Email'
        }


#Data diri
class FarmerForm(forms.ModelForm):
     class Meta:
        model = Farmer
        fields = ['Name', 'FarmerGroup', 'Location']
        labels = {
            'Name': 'Nama Lengkap',
            'Location': 'Lokasi',
            'FarmerGroup': 'Kelompok Tani'
        }
        widgets = {
            'Location': forms.HiddenInput()
        }


class TraderForm(forms.ModelForm):
     class Meta:
        model = Trader
        fields = ['Name', 'Location']
        labels = {
            'Name': 'Nama Lengkap',
            'Location': 'Lokasi',
        }
        widgets = {
            'Location': forms.HiddenInput()
        }


class FactoryForm(forms.ModelForm):
     class Meta:
        model = Factory
        fields = ['FactoryName', 'Location',]
        labels = {
            'FactoryName': 'Nama Perusahaan',
            'Location': 'Lokasi',
        }
        widgets = {
            'Location': forms.HiddenInput()
        }



class DistributorForm(forms.ModelForm):
     class Meta:
        model = Distributor
        fields = ['Name','Location']
        labels = {
            'Name': 'Nama Lengkap',
            'Location': 'Lokasi',
        }
        widgets = {
            'Location': forms.HiddenInput()
        }



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['Name','Location']
        labels = {
            'Name': 'Nama Lengkap',
            'Location': 'Lokasi',
        }
        widgets = {
            'Location': forms.HiddenInput()
        }


#FactoryProcess
class FactoryProcessForm(forms.ModelForm):
    class Meta:
        model = ProductFactory
        fields = [
            'DryingStart', 'DryingEnd', 'PressingDate', 'PackagingDate', 'PackagingType','ProductionCode'
        ]
        widgets = {
            "DryingStart": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "DryingEnd": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "PressingDate": forms.DateInput(attrs={"type": "date"}),
            "PackagingDate": forms.DateInput(attrs={"type": "date"}),
            
        }

