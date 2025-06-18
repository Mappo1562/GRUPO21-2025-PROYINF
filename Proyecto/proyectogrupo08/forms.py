from django import forms
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Profile, Solicitud, Categoria


class RegistroForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']  


class NewRegister(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label="Rol")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Profile.objects.create(user=user, role=self.cleaned_data['role'])
        return user
    

class solicitud_form(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['title', 'content']


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']