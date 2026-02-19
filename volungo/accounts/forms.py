from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class EmailOrUsernameAuthForm(forms.Form):
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        identifier = self.cleaned_data.get('username')
        password   = self.cleaned_data.get('password')

        if identifier and password:
            if '@' in identifier:
                try:
                    validate_email(identifier)
                except DjangoValidationError:
                    raise forms.ValidationError('Please enter a valid email address.')

                try:
                    user = User.objects.get(email=identifier)
                    identifier = user.username
                except User.DoesNotExist:
                    raise forms.ValidationError('No account found with that email.')

            self.user = authenticate(username=identifier, password=password)

            if self.user is None:
                raise forms.ValidationError('Invalid username or password.')

        return self.cleaned_data

    def get_user(self):
        return self.user
