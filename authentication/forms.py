from django import forms
from medical.models import Doctor, Patient
from .models import User

USER_TYPES = (("doctor", "doctor"), ("patient", "patient"))


class RegisterForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=USER_TYPES, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  "password", 'gender', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user
