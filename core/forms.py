from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import Perfil
from django.contrib.auth.forms import UserCreationForm

class UsuarioCadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=20, required=True)
    nivel = forms.ChoiceField(choices=Perfil.NIVEL_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'telefone', 'nivel']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Perfil.objects.create(
                user=user,
                telefone=self.cleaned_data['telefone'],
                nivel=self.cleaned_data['nivel']
            )
        return user


class UsuarioEdicaoForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=20, required=True)
    nivel = forms.ChoiceField(choices=Perfil.NIVEL_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        self.perfil = kwargs.pop('perfil', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            if self.perfil:
                self.perfil.telefone = self.cleaned_data['telefone']
                self.perfil.nivel = self.cleaned_data['nivel']
                self.perfil.save()
        return user

