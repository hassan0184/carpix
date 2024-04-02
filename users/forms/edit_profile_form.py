from django import forms
from users.models import Profile, User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['fullname'] = forms.CharField(initial=self.instance.user.fullname, label='Full Name')
        self.fields['username'] = forms.CharField(initial=self.instance.user.username, label='Username')
        self.fields['email'] = forms.EmailField(initial=self.instance.user.email, label='Email')
        self.fields["phone"]=forms.CharField(initial=self.instance.phone ,label='Contact')
        self.fields["address"]=forms.CharField(initial=self.instance.address ,label='Address')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')
        if username and User.objects.filter(username=username).exclude(username=self.instance.user.username).exists():
            self.add_error('username', "This username is already in use.")
        if email and User.objects.filter(email=email).exclude(email=self.instance.user.email).exists():
            self.add_error('email', "This email is already in use.")
        return cleaned_data

    def save(self, commit=True):    
        profile = super(EditProfileForm, self).save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.fullname=self.cleaned_data["fullname"]
        user.save()
        if commit:
            profile.save()
            user.save()
        return profile