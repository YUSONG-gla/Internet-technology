from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BudgetForm, CategoryForm, LoginForm, TransactionForm, UserRegistrationForm
from .models import Budget, Category, Transaction


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'tracker/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')

            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'tracker/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('login')


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)

    category_id = request.GET.get('category')
    if category_id and category_id != 'all':
        transactions = transactions.filter(category_id=category_id)

    type_filter = request.GET.get('type')
    if type_filter and type_filter != 'all':
        transactions = transactions.filter(type=type_filter)

    date_from = request.GET.get('date_from')
    if date_from:
        transactions = transactions.filter(date__gte=date_from)

    date_to = request.GET.get('date_to')
    if date_to:
        transactions = transactions.filter(date__lte=date_to)

    total_income = transactions.filter(type='Income').aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    total_expense = transactions.filter(type='Expense').aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    balance = total_income - total_expense

    categories = Category.objects.all()
    budget = Budget.objects.filter(user=request.user).order_by('-id').first()

    budget_used = 0
    budget_percentage = 0
    budget_status = None

    if budget and budget.limit_amount > 0:
        today = date.today()

        monthly_expenses = Transaction.objects.filter(
            user=request.user,
            type='Expense',
            date__year=today.year,
            date__month=today.month,
        )

        budget_used = monthly_expenses.aggregate(
            Sum('amount')
        )['amount__sum'] or 0

        budget_percentage = (budget_used / budget.limit_amount) * 100

        if budget_percentage >= 100:
            budget_status = 'exceeded'
        elif budget_percentage >= 80:
            budget_status = 'warning'
        else:
            budget_status = 'safe'
    else:
        budget = None

    context = {
        'transactions': transactions.order_by('-date'),
        'categories': categories,
        'selected_category': category_id if category_id else 'all',
        'selected_type': type_filter if type_filter else 'all',
        'date_from': date_from,
        'date_to': date_to,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'budget': budget,
        'budget_used': budget_used,
        'budget_percentage': budget_percentage,
        'budget_status': budget_status,
    }

    return render(request, 'tracker/dashboard.html', context)


@login_required
def add_transaction(request):
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


@login_required
def set_budget(request):
    budget = Budget.objects.filter(user=request.user).order_by('-id').first()

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            budget_obj = form.save(commit=False)
            budget_obj.user = request.user
            budget_obj.period = 'Monthly'
            budget_obj.save()
            messages.success(request, 'Monthly budget updated successfully.')
            return redirect('dashboard')
    else:
        form = BudgetForm(instance=budget)

    return render(request, 'tracker/set_budget.html', {'form': form})


@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New category added successfully!')
            return redirect('add_transaction')
    else:
        form = CategoryForm()

    return render(request, 'tracker/add_category.html', {'form': form})


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user,
    )

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted.')
        return redirect('dashboard')

    return redirect('dashboard')


@login_required
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(
        Transaction,
        id=transaction_id,
        user=request.user,
    )

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            updated_transaction = form.save(commit=False)
            updated_transaction.user = request.user
            updated_transaction.save()
            messages.success(request, 'Transaction updated successfully.')
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'tracker/edit_transaction.html', {
        'form': form,
        'transaction': transaction,
    })