from django import forms

from .models import Client, Expense, ExpenseCategory, Income


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "client_type", "contacts"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ["name"]


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["client", "amount", "currency", "date", "description"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
        labels = {"client": "Клиент"}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["client"].queryset = Client.objects.filter(user=user)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Сумма должна быть больше нуля.")
        return amount


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["category", "amount", "date", "description"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
        labels = {"category": "Категория"}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["category"].queryset = ExpenseCategory.objects.filter(user=user)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Сумма должна быть больше нуля.")
        return amount