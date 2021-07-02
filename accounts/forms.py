from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import User, Student, Union


class StudentSignUpForm(UserCreationForm):
    phone_number = forms.CharField(label="Phone Number", widget=forms.NumberInput(attrs={'class': 'input'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        return user


class UnionSignUpForm(UserCreationForm):
    username = forms.CharField(label="Union Name")
    first_name = forms.CharField(label="Short Name", widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField()
    phone_number = forms.CharField(label="Phone Number", widget=forms.NumberInput(attrs={'class': 'input'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'email', 'phone_number',  'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = False
        user.is_union = True
        user.is_staff = False
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        union = Union.objects.create(user=user)
        return user
