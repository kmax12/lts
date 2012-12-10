from registration.forms import RegistrationForm
from django import forms
from lifetime.models import *

class UserRegistrationForm(RegistrationForm):
    code = forms.CharField(min_length=8, max_length=8, required=False, label="Gift Code (optional)")

    def clean_code(self):
        data = self.cleaned_data['code']

        # Only do something if both fields are valid so far.
        if GiftModel.objects.filter(code=data, subscription=None).count() != 1:
            raise forms.ValidationError("Gift code not valid.")

        return data
