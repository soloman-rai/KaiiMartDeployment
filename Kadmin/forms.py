from django import forms

from django.contrib.auth import get_user_model
from manager.models import Manager


USER = get_user_model()

class ManagerRegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = USER
        fields = ('username', 'email', )

    def clean_password(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ManagerRegisterForm, self).save(commit=False)
        username = user.username
        user.set_password(self.cleaned_data["password1"])
        user.is_manager = True
        user.is_active = True
        if commit:
            user.save()
        Manager.objects.create(user=user, username=username)
        return user