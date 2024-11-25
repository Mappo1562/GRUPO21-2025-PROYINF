from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Profile, Solicitud


class RegistroForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']  
"""
class NewRegister(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','password1','password2']
    
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
"""

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