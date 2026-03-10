# Django Core Imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# [FIXED] Added TransactionForm here to prevent NameError!
from .forms import UserRegistrationForm, LoginForm, TransactionForm, BudgetForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Local App Imports (Models & Forms)
from .models import Transaction, Budget
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
# [Intent] The Dashboard is the core "View Data" (M4) requirement.
# Decision: Use @login_required decorator to ensure the page is inaccessible to unauthorized users.
@login_required
def dashboard(request):
    """
    Logic to aggregate financial data for the currently logged-in user.
    Decision: Data is filtered by 'request.user' to ensure strict data isolation (Privacy).
    """
    user_transactions = Transaction.objects.filter(user=request.user)

    # Calculate totals using DB aggregation for better sustainability/performance
    total_income = user_transactions.filter(type='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = user_transactions.filter(type='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses

    # Fetch recent history and budget status (Supports S1 requirement)
    recent_transactions = user_transactions.order_by('-date')[:5]
    budget = Budget.objects.filter(user=request.user).first()

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'budget': budget,
    }
    return render(request, 'tracker/dashboard.html', context)


# [Intent] Handle the creation of new financial records (M2 requirement).
# Decision: Function name matches the pointer in urls.py (views.add_transaction).
@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            # [Decision] Crucial Security Step: Manually assign the transaction to the 
            # logged-in user to prevent data injection vulnerabilities.
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    
    return render(request, 'tracker/add_transaction.html', {'form': form})
# [Intent] Allow users to set or update their spending budget (Supports S1 requirement).
# [Decision] Use get_or_create to fetch the user's existing budget, or create a default one 
# if it doesn't exist. This ensures we don't duplicate budget records for a single user.
@login_required
def set_budget(request):
    # Fetch existing budget or create a new one with a default limit of 0
    budget, created = Budget.objects.get_or_create(
        user=request.user, 
        defaults={'limit_amount': 0, 'period': 'Monthly'}
    )
    
    if request.method == 'POST':
        # Pass the instance to the form so it updates the existing record instead of creating a new one
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your budget has been successfully updated!')
            return redirect('dashboard')
    else:
        form = BudgetForm(instance=budget)
    
    return render(request, 'tracker/set_budget.html', {'form': form})


# [Intent] Allow users to add new categories for organizing transactions (Supports M3 requirement).
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New category added successfully!')
            # Redirect back to the add transaction page so they can use the new category immediately
            return redirect('add_transaction')
    else:
        form = CategoryForm()
        
    return render(request, 'tracker/add_category.html', {'form': form})