from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Entity: Category
    Intent: Allows users to group their transactions (e.g., Food, Transport).
    This supports the 'M3' requirement (categorising expenses) and ensures data normalization.
    """
    # Category Name from ER Diagram
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        # Django automatically pluralizes model names, adding this fixes the spelling in Admin
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Transaction(models.Model):
    """
    Entity: Transaction
    Intent: Stores individual financial records. 
    Decision: Linked via ForeignKey to the User model to ensure data privacy (users can only access 
    their own records), fulfilling the core database interaction requirement (M4).
    """
    # Choices for the 'Type' attribute defined in the ER Diagram
    TYPE_CHOICES = (
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    )

    # Relationships (1-to-N) based on ER Diagram logically
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Attributes from ER Diagram
    # Decision: DecimalField is used instead of FloatField to prevent floating-point precision loss 
    # in financial calculations, which is critical for a finance tracker.
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)
    date = models.DateField()
    
    # Optional description
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        # Decision: Order records by date descending. This optimizes database queries 
        # when fetching "Recent Transactions" for the user dashboard.
        ordering = ['-date']

    def __str__(self):
        return f"{self.type} - {self.amount} on {self.date}"


class Budget(models.Model):
    """
    Entity: Budget
    Intent: Allows users to set spending limits. This provides the foundational data 
    needed to calculate remaining budget on the monitoring dashboard (S1 requirement).
    """
    PERIOD_CHOICES = (
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    )

    # Each user can set their own budget limits
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    
    # Attributes from ER Diagram
    limit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='Monthly')

    def __str__(self):
        return f"{self.user.username}'s {self.period} Budget: {self.limit_amount}"
