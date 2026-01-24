from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PayrollViewSet, InvoiceViewSet, ExpenseViewSet,
    RevenueViewSet, BudgetViewSet, FinancialReportViewSet
)

router = DefaultRouter()
router.register(r'payroll', PayrollViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'revenue', RevenueViewSet)
router.register(r'budgets', BudgetViewSet)
router.register(r'reports', FinancialReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]