from django import forms
from django.forms import TextInput

from .models import CustomUser, TaskModel
from .widgets import DatePickerInput


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Email address")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Password")


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Use CustomUser if you created one
        fields = ['first_name', 'last_name', 'username', 'email', 'manager']
        labels = {'first_name': "First Name", 'last_name': "Last Name", "username": "Username", "email": "Email",
                  "manager": "Manager"}
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control"
            }),
            'last_name': TextInput(attrs={
                'class': "form-control"
            }),
            'username': TextInput(attrs={
                'class': "form-control"
            }),
            'email': TextInput(attrs={
                'class': "form-control"
            }),
            'manager': forms.Select(attrs={
                'class': "form-control"
            }),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        exclude = ['is_in_progress', 'is_completed']
        fields = '__all__'

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Title")
    due_date = forms.DateField(
        label="Due Date",
        widget=DatePickerInput(attrs={'class': 'form-control'})
    )
    assigned_to = forms.ChoiceField(label="Assigned To", widget=forms.Select(attrs={'class': 'form-control'}))
    priority = forms.ChoiceField(label="Priority", widget=forms.Select(attrs={'class': 'form-control'}))


class SearchForm(forms.Form):
    user = forms.ChoiceField(label="User", widget=forms.Select(attrs={'class': 'form-control'}))
