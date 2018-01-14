from django import forms
from models import Equipo, Deporte, Usuario

class create_user(forms.Form):
    user_name = forms.CharField(max_length=20, required = True, label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, max_length=200)
    repeat_password = forms.CharField(widget=forms.PasswordInput, max_length=200)
    name = forms.CharField(max_length=100, required = True, label='Nombre')
    surname = forms.CharField(max_length=100, required=True, label='Apellidos')
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=300, required=True, label='Direccion')

class select_friend_form(forms.Form):
    usuarios = forms.ModelChoiceField(queryset=Usuario.objects.all())

class search_user_form(forms.Form):
    user_name = forms.CharField(max_length=20, required=True, label='Introduzca el nombre de usuario')

class search_notice_form(forms.Form):
    param = forms.CharField(max_length=60, required=True, label='Introduzca la palabra clave')