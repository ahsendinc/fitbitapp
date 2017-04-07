
# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'email')

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('firstname', 'lastname', 'fitbitid')

from django import forms            
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import UserCreationForm      

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    firstname = forms.CharField(required = True)
    lastname = forms.CharField(required = True)

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super(MyRegistrationForm, self).clean()
        temp_password = cleaned_data['password1']
        if "password" in temp_password:
            self.add_error('password1', 'Your password is too simple.')

        return cleaned_data

    def save(self,commit = True):   
        user = super(MyRegistrationForm, self).save(commit = False)
        #user_profile = UserProfile(user=user, email = self.cleaned_data['email'], firstname = self.cleaned_data['firstname'],
        #lastname = self.cleaned_data['lastname'], fitbitid = self.cleaned_data['fitbitid'])
        user.email = self.cleaned_data['email']
        user.firstname = self.cleaned_data['firstname']
        user.lastname = self.cleaned_data['lastname']

        if commit:
            user.save()

        return user