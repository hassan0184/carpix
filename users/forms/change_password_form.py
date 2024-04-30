from typing import Any
from django import forms
from users.models import Profile, User


class ChangePasswordForm(forms.Form):
    old_password=forms.CharField()
    new_password=forms.CharField()
    confirm_password=forms.CharField()

    def clean(self):
        if len(self.cleaned_data.get("password")) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        has_uppercase = any(char.isupper() for char in self.cleaned_data.get("password"))
        has_lowercase = any(char.islower() for char in self.cleaned_data.get("password"))
        has_numeric = any(char.isdigit() for char in self.cleaned_data.get("password"))
        if not (has_uppercase and has_lowercase and has_numeric):
        
            raise forms.ValidationError("Password must contain both uppercase and lowercase characters and and one numeric digit")

        if self.cleaned_data.get("new_password") != self.cleaned_data.get("confirm_password"):
            raise forms.ValidationError("new password and confirm password must match")
        return self.cleaned_data