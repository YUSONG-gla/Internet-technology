from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Transaction, Budget
from decimal import Decimal
import datetime

class TrackerModelTests(TestCase):
    def setUp(self):
        # 建立测试所需的基础数据 (User 和 Category)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Groceries')

    def test_category_creation_and_str(self):
        """测试 Category 模型的创建和字符串表示是否正确"""
        self.assertEqual(self.category.name, 'Groceries')
        self.assertEqual(str(self.category), 'Groceries')

    def test_transaction_creation_and_str(self):
        """测试 Transaction 模型的创建和字符串表示"""
        transaction = Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('45.50'),
            type='Expense',
            date=datetime.date(2026, 3, 15),
            description='Weekly shopping'
        )
        self.assertEqual(transaction.amount, Decimal('45.50'))
        self.assertEqual(transaction.type, 'Expense')
        # 测试你定义的 __str__ 方法: f"{self.type} - {self.amount} on {self.date}"
        self.assertEqual(str(transaction), 'Expense - 45.50 on 2026-03-15')

    def test_transaction_ordering(self):
        """测试 Transaction 模型 Meta 类中的 ['-date'] 排序是否生效"""
        Transaction.objects.create(
            user=self.user, category=self.category, amount=Decimal('10.00'),
            type='Expense', date=datetime.date(2026, 3, 10)
        )
        Transaction.objects.create(
            user=self.user, category=self.category, amount=Decimal('20.00'),
            type='Expense', date=datetime.date(2026, 3, 15)  # 这个日期更晚
        )
        
        # 获取所有记录，预期最新的日期应该排在第一位
        transactions = Transaction.objects.all()
        self.assertEqual(transactions[0].date, datetime.date(2026, 3, 15))

    def test_budget_creation_and_str(self):
        """测试 Budget 模型的创建和字符串表示"""
        budget = Budget.objects.create(
            user=self.user,
            limit_amount=Decimal('500.00'),
            period='Monthly'
        )
        self.assertEqual(budget.limit_amount, Decimal('500.00'))
        # 测试你定义的 __str__ 方法: f"{self.user.username}'s {self.period} Budget: {self.limit_amount}"
        self.assertEqual(str(budget), "testuser's Monthly Budget: 500.00")