from django import forms
from .models import Transaction, Budget
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class TransactionForm(forms.ModelForm):
    """
    Intent: Form to handle user input for creating or editing transactions.
    Using ModelForm ensures built-in validation (e.g., ensuring amount is a decimal) 
    and fulfills the requirement for meaningful user input processing.
    """
    class Meta:
        model = Transaction
        # We exclude 'user' because we will automatically set it to the currently logged-in user in the view
        fields = ['amount', 'type', 'category', 'date', 'description']
        
        # Adding HTML5 widgets to improve UI/UX (Look and Feel)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Optional notes...'}),
        }

class BudgetForm(forms.ModelForm):
    """
    Intent: Form for users to set their spending limits.
    """
    class Meta:
        model = Budget
        fields = ['limit_amount', 'period']
        widgets = {
            'limit_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'period': forms.Select(attrs={'class': 'form-control'}),
        }
# ---------- Form for user authentication (Supports M1 Requirement) ----------
class LoginForm(forms.Form):
    """
    Intent: Handle user login securely.
    """
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )

class UserRegistrationForm(forms.ModelForm):
    """
    Intent: Handle new user registration. 
    Uses ModelForm based on Django's built-in User model for security.
    """
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }

# Alias for backward compatibility
RegisterForm = UserRegistrationForm