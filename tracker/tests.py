from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Transaction, Budget


class CategoryModelTest(TestCase):
    """Category 模型测试"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name="Food",
            description="Food and groceries"
        )
    
    def test_category_creation(self):
        """测试分类创建"""
        self.assertEqual(self.category.name, "Food")
        self.assertEqual(str(self.category), "Food")


class TransactionModelTest(TestCase):
    """Transaction 模型测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Food")
        self.transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=100.00,
            transaction_type='expense',
            description='Lunch'
        )
    
    def test_transaction_creation(self):
        """测试交易记录创建"""
        self.assertEqual(self.transaction.user.username, 'testuser')
        self.assertEqual(self.transaction.amount, 100.00)
        self.assertEqual(self.transaction.transaction_type, 'expense')
    
    def test_transaction_string_representation(self):
        """测试交易记录字符串表示"""
        expected = f"testuser - 100.00 (支出)"
        self.assertEqual(str(self.transaction), expected)


class BudgetModelTest(TestCase):
    """Budget 模型测试"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name="Food")
        from datetime import date
        self.budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            limit=500.00,
            month=date(2023, 1, 1)
        )
    
    def test_budget_creation(self):
        """测试预算创建"""
        self.assertEqual(self.budget.user.username, 'testuser')
        self.assertEqual(self.budget.limit, 500.00)
