from django import forms

class create_user(forms.Form):
    user_name = forms.CharField(max_length=20, required = True, label='Nombre de usuario')
    password = forms.CharField(widget=forms.PasswordInput, max_length=200)
    name = forms.CharField(max_length=100, required = True, label='Nombre')
    surname = forms.CharField(max_length=100, required=True, label='Apellidos')
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=300, required=True, label='Direccion')
