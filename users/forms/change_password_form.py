from typing import Any
from django import forms
from users.models import Profile, User


class ChangePasswordForm(forms.Form):
    old_password=forms.CharField()
    new_password=forms.CharField()
    confirm_password=forms.CharField()

    def clean(self):
        if self.cleaned_data.get("new_password") != self.cleaned_data.get("confirm_password"):
            raise forms.ValidationError("new password and confirm password must match")
        return self.cleaned_data