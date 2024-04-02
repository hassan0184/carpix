from django import forms
from users.models import User


class UserSignupForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "password", "email", "fullname"]

    def clean(self):
        if User.objects.filter(username=self.cleaned_data.get("username")).exists():
            raise forms.ValidationError("User with the same username already exists")
        if User.objects.filter(email=self.cleaned_data.get("email")).exists():
            raise forms.ValidationError("User with the same email already exists")
        if self.cleaned_data.get("password") != self.cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Password and confirm password must match")
        return self.cleaned_data
