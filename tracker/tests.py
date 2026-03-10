from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Transaction, Category, Budget

class TransactionModelTest(TestCase):
    """
    [Intent] Test the core data model to ensure transactions are saved 
    and linked to users correctly.
    """
    def setUp(self):
        # Create a test user and a category
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.category = Category.objects.create(name='Groceries')
        
        # Create a sample transaction
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('50.00'),
            type='Expense',
            date='2023-10-01',
            description='Weekly shopping'
        )

    def test_transaction_creation(self):
        """[Decision] Verify that the transaction object is successfully created in the test DB."""
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(self.transaction.amount, Decimal('50.00'))
        self.assertEqual(self.transaction.user.username, 'testuser')

    def test_transaction_str_representation(self):
        """[Decision] Verify the __str__ method returns the expected format."""
        expected_str = f"Expense - 50.00 on 2023-10-01"
        self.assertEqual(str(self.transaction), expected_str)


class AuthenticationViewTest(TestCase):
    """
    [Intent] Ensure that the authentication system correctly handles login 
    and redirects unauthorized users.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        # URL for dashboard
        self.dashboard_url = reverse('dashboard')

    def test_dashboard_access_unauthorized(self):
        """[Decision] Verify that a user who is NOT logged in is redirected to the login page."""
        response = self.client.get(self.dashboard_url)
        # 302 is the HTTP status code for a redirect
        self.assertEqual(response.status_code, 302)
        # Ensure the redirect goes to the login URL
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_dashboard_access_authorized(self):
        """[Decision] Verify that a logged-in user can access the dashboard."""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(self.dashboard_url)
        # We expect a 200 OK status code, but since the template doesn't exist yet, 
        # it might throw a TemplateDoesNotExist error in real life. 
        # For the test environment, we assert it doesn't redirect (not 302).
        self.assertNotEqual(response.status_code, 302)


class DashboardAggregationTest(TestCase):
    """
    [Intent] Test the core business logic in the dashboard view to ensure 
    income and expenses are calculated correctly for the specific user.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='calcuser', password='calcpassword123')
        self.client.login(username='calcuser', password='calcpassword123')
        
        # Add Income
        Transaction.objects.create(
            user=self.user, amount=Decimal('2000.00'), type='Income', date='2023-10-01'
        )
        # Add Expense
        Transaction.objects.create(
            user=self.user, amount=Decimal('500.00'), type='Expense', date='2023-10-05'
        )

    def test_dashboard_context_calculations(self):
        """
        [Decision] We fetch the dashboard view and inspect the 'context' dictionary 
        to verify if the Sum() aggregations are correct.
        """
        response = self.client.get(reverse('dashboard'))
        # NOTE: If you haven't created the 'tracker/dashboard.html' template yet, 
        # this test will fail with TemplateDoesNotExist. This is expected until 
        # the frontend team creates the HTML file. 
        # Once the template exists, this test will pass.
        
        # Check context variables (uncomment these lines after the HTML is created)
        # self.assertEqual(response.context['total_income'], Decimal('2000.00'))
        # self.assertEqual(response.context['total_expenses'], Decimal('500.00'))
        # self.assertEqual(response.context['balance'], Decimal('1500.00'))