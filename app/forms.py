
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
    fitbitid = forms.CharField(required = True)

    class Meta:
        model = User
        fields = ('username','email', 'password1', 'password2')        

    def save(self,commit = True):   
        user = super(MyRegistrationForm, self).save(commit = False)
        #user_profile = UserProfile(user=user, email = self.cleaned_data['email'], firstname = self.cleaned_data['firstname'],
        #lastname = self.cleaned_data['lastname'], fitbitid = self.cleaned_data['fitbitid'])
        user.email = self.cleaned_data['email']
        user.firstname = self.cleaned_data['firstname']
        user.lastname = self.cleaned_data['lastname']
        user.fitbitid = self.cleaned_data['fitbitid']

        if commit:
            user.save()

        return user