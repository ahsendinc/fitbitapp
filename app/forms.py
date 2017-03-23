from django import forms
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('firstname', 'lastname', 'fitbitid')