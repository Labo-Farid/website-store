from django import forms
from .models import Signup


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "Entrer votre adresse mail",
    }), label="")

    class Meta:
        model = Signup
        fields = ('email', )
