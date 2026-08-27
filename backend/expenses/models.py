from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="categories"
    )
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expenses"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="expenses"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    expense_date = models.DateField()

    def __str__(self):
        return f"{self.description} - {self.amount}"