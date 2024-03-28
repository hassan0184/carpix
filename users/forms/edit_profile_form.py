from django import forms
from users.models import Profile, User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(initial=self.instance.user.username, label='Username')
        self.fields['email'] = forms.EmailField(initial=self.instance.user.email, label='Email')

    def clean(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if User.objects.filter(email=email).exclude(username=self.instance.user.username).exists():
            raise forms.ValidationError("This email address is already in use.")
        if User.objects.filter(username=username).exclude(email=self.instance.user.email).exists():
            raise forms.ValidationError("This username is already in use.")
        return self.cleaned_data


    def save(self, commit=True):
        profile = super(EditProfileForm, self).save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            profile.save()
            user.save()
        return profile