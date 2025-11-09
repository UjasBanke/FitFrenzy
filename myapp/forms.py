from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Create password'}),
        label="Create password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label="Confirm password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_username(self):
        """
        Allow spaces in usernames and prevent accidental trimming.
        Also ensure username uniqueness.
        """
        username = self.cleaned_data.get('username', '').strip()  # Keep internal spaces
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean(self):
        """
        Confirm both passwords match.
        """
        cleaned = super().clean()
        p1 = cleaned.get("password")
        p2 = cleaned.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Passwords do not match")

        return cleaned


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['dob', 'height_cm', 'weight_kg']
