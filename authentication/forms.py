from django import forms
from utils.validate_password import validate_password_strength
from .models import User

USER_TYPES = (("doctor", "doctor"), ("patient", "patient"))


class RegisterForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=USER_TYPES, required=True)
    password = forms.CharField(max_length=100, min_length=6,
                               widget=forms.PasswordInput(
                                   attrs={"placeholder": "Enter your password"}),
                               validators=[validate_password_strength],
                               help_text="Password length must be 8 chars at least, contain at least one uppercase letter, one lowercase letter, one number and at least one special character (@, #, $, %, ^, &, +, =)"

                               )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user


class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=100, required=True,
                               widget=forms.PasswordInput(
                                   attrs={
                                       "placeholder": "Enter your password"}
                               ),
                               )

    class Meta:
        model = User
        fields = ['email']


class PasswordResetCodeForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)


class ChangePasswordResetCodeForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput(
        attrs={"readonly": "readonly"}))
    code = forms.CharField(max_length=6, required=True, label="Reset code",
                           widget=forms.TextInput(
                               attrs={'placeholder': "Enter reset code"})
                           )
    new_password = forms.CharField(max_length=100, required=True,
                                   widget=forms.PasswordInput(
                                       attrs={
                                           "placeholder": "Enter new password"}
                                   ),
                                   validators=[validate_password_strength],
                                   help_text="Password length must be 8 chars at least, contain at least one uppercase letter, one lowercase letter, one number and at least one special character (@, #, $, %, ^, &, +, =)"
                                   )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if request and 'reset_email' in request.session:
            self.fields['email'].initial = request.session['reset_email']
