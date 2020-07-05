from ebsite.models import *
from django import forms
from django.forms import ModelForm,Textarea

class ContactForm(forms.Form):
    sujet = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    envoyeur = forms.EmailField(label="Votre adresse e-mail")
    renvoi = forms.BooleanField(help_text="Cochez si vous souhaitez obtenir une copie du mail envoyé.", required=False)

class RegisterForm(ModelForm):
    first_name = forms.CharField(label='Votre prénom', required=True)
    last_name = forms.CharField(label='Votre nom', required=True)
    email = forms.EmailField(label='Votre adresse e-mail', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class RegisterFormUpdate(ModelForm):
    first_name = forms.CharField(label='Votre prénom', required=True)
    last_name = forms.CharField(label='Votre nom', required=True)
    email = forms.EmailField(label='Votre adresse e-mail', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AddAddress(ModelForm):
    class Meta:
        model = Contact
        fields = [ 'prenom_contact', 'nom_contact', 'company', 'rue',
                  'codepostal', 'ville', 'telephone']


class MurForm(ModelForm):
    class Meta:
        model = mur
        fields = ['message','pseudo']
        widgets = {
            'message': Textarea(attrs={'cols': 25, 'rows': 7}),
            'pseudo': Textarea(attrs={'cols': 25, 'rows': 1}),
        }