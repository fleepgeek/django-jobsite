from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
# from django.contrib.admin.widgets import AdminDateWidget

from .models import Applicant, Company

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)

    def clean_password2(self):
        data = self.cleaned_data
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords you entered are not the same')
        return password1

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'is_active', 'is_superuser',)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ApplicantSignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password2(self):
        data = self.cleaned_data
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords you entered are not the same')
        return password1

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_applicant = True
        user.save()
        applicant = Applicant.objects.create(user=user)
        return user

class ApplicantForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Applicant
        fields = ('date_of_birth','location', 'gender', 'about', 'years_of_exp')


class CompanySignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    company_name = forms.CharField(label='Company Name')

    class Meta:
        model = User
        fields = ('full_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password2(self):
        data = self.cleaned_data
        password1 = data.get('password1')
        password2 = data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('The passwords you entered are not the same')
        return password1

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_employer = True
        user.save()
        company_name = self.cleaned_data.get('company_name')
        company = Company.objects.create(user=user, name=company_name)
        return user

class LoginForm(AuthenticationForm):
    # username is used here because we set the USERNAME_FIELD = email 
    # in our custom User model
    username = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )