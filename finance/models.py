from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    TYPE_CHOICES = [
        ("individual", "Физлицо"),
        ("company", "Юрлицо / ИП"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients")
    name = models.CharField("Название", max_length=200)
    client_type = models.CharField("Тип", max_length=20, choices=TYPE_CHOICES)
    contacts = models.CharField("Контакты", max_length=300, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incomes")
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="incomes")
    amount = models.DecimalField("Сумма", max_digits=12, decimal_places=2)
    currency = models.CharField("Валюта", max_length=3, default="RUB")
    date = models.DateField("Дата")
    description = models.CharField("Описание", max_length=300, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.amount} {self.currency} от {self.client}"


class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField("Название", max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Expense categories"

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT, related_name="expenses")
    amount = models.DecimalField("Сумма", max_digits=12, decimal_places=2)
    date = models.DateField("Дата")
    description = models.CharField("Описание", max_length=300, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.amount} ({self.category})"