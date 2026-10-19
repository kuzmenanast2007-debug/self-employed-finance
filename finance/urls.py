from django.urls import path

from . import views

urlpatterns = [
    path("clients/", views.client_list, name="client_list"),
    path("clients/new/", views.client_create, name="client_create"),
    path("clients/<int:pk>/delete/", views.client_delete, name="client_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/new/", views.category_create, name="category_create"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("income/", views.income_list, name="income_list"),
    path("income/new/", views.income_create, name="income_create"),
    path("income/<int:pk>/delete/", views.income_delete, name="income_delete"),
    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/new/", views.expense_create, name="expense_create"),
    path("expenses/<int:pk>/delete/", views.expense_delete, name="expense_delete"),
]