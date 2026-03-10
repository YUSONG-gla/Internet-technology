from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, LoginForm

# Logic to handle user registration securely.
# Decision: Uses custom UserRegistrationForm to capture email and username, 
# then manually sets the password using set_password to ensure encryption/hashing.
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # [Decision] Security requirement: Ensure passwords are not stored in plain text.
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'tracker/register.html', {'form': form})

# Authenticate user credentials and start a session.
# Decision: Uses Django's built-in authenticate() to verify credentials against the DB.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to dashboard upon successful authentication
                return redirect('dashboard')
            else:
                # Provide feedback for security failures without exposing specific details
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'tracker/login.html', {'form': form})

# [Intent] Log out user and clear session data.
def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')