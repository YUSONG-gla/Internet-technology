from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from .models import Transaction, Category, Budget
from .forms import LoginForm, TransactionForm, RegisterForm


def login_view(request):
    """用户登录视图"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'tracker/login.html', {'form': form})


def register_view(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'tracker/register.html', {'form': form})


def logout_view(request):
    """用户登出视图"""
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """用户仪表板"""
    user = request.user
    transactions = Transaction.objects.filter(user=user).order_by('-date')[:10]
    
    income = Transaction.objects.filter(
        user=user, transaction_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    expense = Transaction.objects.filter(
        user=user, transaction_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    balance = income - expense
    
    context = {
        'transactions': transactions,
        'income': income,
        'expense': expense,
        'balance': balance,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required(login_url='login')
def add_transaction(request):
    """添加交易记录"""
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form})
