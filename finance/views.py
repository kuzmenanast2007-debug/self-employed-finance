from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, ClientForm, ExpenseForm, IncomeForm
from .models import Client, Expense, ExpenseCategory, Income


@login_required
def client_list(request):
    clients = Client.objects.filter(user=request.user)
    return render(request, "finance/client_list.html", {"clients": clients})


@login_required
def client_create(request):
    form = ClientForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        client = form.save(commit=False)
        client.user = request.user
        client.save()
        messages.success(request, "Клиент добавлен.")
        return redirect("client_list")
    return render(request, "finance/form.html", {"form": form, "title": "Новый клиент"})


@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk, user=request.user)
    if request.method == "POST":
        try:
            client.delete()
            messages.success(request, "Клиент удалён.")
        except ProtectedError:
            messages.error(request, "Нельзя удалить клиента: по нему есть доходы.")
    return redirect("client_list")


@login_required
def category_list(request):
    categories = ExpenseCategory.objects.filter(user=request.user)
    return render(request, "finance/category_list.html", {"categories": categories})


@login_required
def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        category.save()
        messages.success(request, "Категория добавлена.")
        return redirect("category_list")
    return render(request, "finance/form.html", {"form": form, "title": "Новая категория"})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk, user=request.user)
    if request.method == "POST":
        try:
            category.delete()
            messages.success(request, "Категория удалена.")
        except ProtectedError:
            messages.error(request, "Нельзя удалить категорию: в ней есть расходы.")
    return redirect("category_list")


@login_required
def income_list(request):
    incomes = Income.objects.filter(user=request.user).select_related("client")
    return render(request, "finance/income_list.html", {"incomes": incomes})


@login_required
def income_create(request):
    form = IncomeForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        income = form.save(commit=False)
        income.user = request.user
        income.save()
        messages.success(request, "Доход добавлен.")
        return redirect("income_list")
    return render(request, "finance/form.html", {"form": form, "title": "Новый доход"})


@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == "POST":
        income.delete()
        messages.success(request, "Доход удалён.")
    return redirect("income_list")


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).select_related("category")
    return render(request, "finance/expense_list.html", {"expenses": expenses})


@login_required
def expense_create(request):
    form = ExpenseForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        messages.success(request, "Расход добавлен.")
        return redirect("expense_list")
    return render(request, "finance/form.html", {"form": form, "title": "Новый расход"})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Расход удалён.")
    return redirect("expense_list")