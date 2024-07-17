from dataclasses import fields
from distutils.command.clean import clean
from django import forms
from .models import Formlar
from django.conf import settings
from django.contrib.admin import widgets
class ConsentForm(forms.ModelForm):

    class Meta:
        model = Formlar
        fields = [

             'ad', 'soyad', 'email', 'cepno', 'iys_sms', 'iys_arama', 'iys_email', 'k_aydinlatmaMetin'

        ]

        labels = {
            "ad": "Ad",
            "soyad": "Soyad",
            "email": "E-posta",
            "cepno": "Cep No",
            "iys_sms": "Sms",
            "iys_arama": "Arama",
            "iys_email": "E-posta",
            "k_aydinlatmaMetin": "Aydınlatma metnin de belirtilen kapsam, amaç ve süre dahilinde kişisel verilerimin işlenmesini kabul ediyorum.",
            
            
        }
        CHOICES = [(True ,'Evet'),(False ,'Hayır')]
        widgets = {
            "ad": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "soyad": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "email": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "cepno": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "iys_sms": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked", 'checked': True}),
            "iys_arama": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked", 'checked':True}),
            "iys_email": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked", 'checked':True}),
            "k_aydinlatmaMetin": forms.CheckboxInput(attrs={"class": "form-check-input",'checked': True}),
        }
        help_texts = {
            "iys_sms": "",
            "iys_arama": "",
            "iys_email": "",
            "k_aydinlatmaMetin": "",
            
            
        }


class ConsentFormWo(forms.ModelForm):

    class Meta:
        model = Formlar
        fields = [

             'ad', 'soyad', 'iys_sms', 'iys_arama', 'iys_email', 'k_aydinlatmaMetin'

        ]

        labels = {
            "ad": "Ad",
            "soyad": "Soyad",
            "iys_sms": "Sms",
            "iys_arama": "Arama",
            "iys_email": "E-posta",
            "k_aydinlatmaMetin": "Aydınlatma metnin de belirtilen kapsam, amaç ve süre dahilinde kişisel verilerimin işlenmesini kabul ediyorum.",


        }
        CHOICES = [(True ,'Evet'),(False ,'Hayır')]
        widgets = {
            "ad": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "soyad": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "iys_sms": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked", 'disabled': True}),
            "iys_arama": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked", 'disabled':True}),
            "iys_email": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked", 'disabled':True}),
            "k_aydinlatmaMetin": forms.CheckboxInput(attrs={"class": "form-check-input",'disabled': True}),
        }
        help_texts = {
            "iys_sms": "",
            "iys_arama": "",
            "iys_email": "",
            "k_aydinlatmaMetin": "",


        }


class ConsentFormWoEmail(forms.ModelForm):

    class Meta:
        model = Formlar
        fields = [

             'ad', 'soyad', 'cepno', 'iys_sms', 'iys_arama', 'k_aydinlatmaMetin'

        ]

        labels = {
            "ad": "Ad",
            "soyad": "Soyad",
            "email": "E-posta",
            "cepno": "Cep No",
            "iys_sms": "Sms",
            "iys_arama": "Arama",
            "k_aydinlatmaMetin": "Aydınlatma metnin de belirtilen kapsam, amaç ve süre dahilinde kişisel verilerimin işlenmesini kabul ediyorum.",


        }
        CHOICES = [(True ,'Evet'),(False ,'Hayır')]
        widgets = {
            "ad": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "soyad": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "cepno": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "iys_sms": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked", 'checked': True}),
            "iys_arama": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked", 'checked':True}),
            "k_aydinlatmaMetin": forms.CheckboxInput(attrs={"class": "form-check-input",'checked': True}),
        }
        help_texts = {
            "iys_sms": "",
            "iys_arama": "",
            "k_aydinlatmaMetin": "",


        }


class ConsentFormWoCep(forms.ModelForm):

    class Meta:
        model = Formlar
        fields = [

             'ad', 'soyad', 'email', 'iys_email', 'k_aydinlatmaMetin'

        ]

        labels = {
            "ad": "Ad",
            "soyad": "Soyad",
            "email": "E-posta",
            "iys_email": "E-posta",
            "k_aydinlatmaMetin": "Aydınlatma metnin de belirtilen kapsam, amaç ve süre dahilinde kişisel verilerimin işlenmesini kabul ediyorum.",


        }
        CHOICES = [(True ,'Evet'),(False ,'Hayır')]
        widgets = {
            "ad": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "soyad": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "email": forms.TextInput(attrs={'disabled': True, 'default': True, 'class': 'form-control'} ),
            "iys_email": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked", 'checked':True}),
            "k_aydinlatmaMetin": forms.CheckboxInput(attrs={"class": "form-check-input",'checked': True}),
        }
        help_texts = {
            "iys_email": "",
            "k_aydinlatmaMetin": "",


        }
