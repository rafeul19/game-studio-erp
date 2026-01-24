from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Payroll, Invoice, Expense, Revenue, 
    Budget, FinancialReport
)

User = get_user_model()


class PayrollSerializer(serializers.ModelSerializer):
    """Payroll record serializer"""
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    month_display = serializers.SerializerMethodField()

    class Meta:
        model = Payroll
        fields = [
            'id', 'employee', 'employee_name', 'employee_id', 'month', 'month_display',
            'base_salary', 'bonuses', 'deductions', 'overtime_hours',
            'overtime_rate', 'net_salary', 'paid_date', 'status', 
            'status_display', 'payment_method', 'payment_method_display',
            'bank_account', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_month_display(self, obj):
        return obj.month.strftime('%B %Y')


class InvoiceSerializer(serializers.ModelSerializer):
    """Invoice serializer"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    days_overdue = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    amount_paid = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True, source='total_paid'
    )

    class Meta:
        model = Invoice
        fields = [
            'id', 'project', 'project_name', 'invoice_number', 'client_name',
            'client_email', 'client_address', 'amount', 'tax_rate', 'tax_amount',
            'total_amount', 'issue_date', 'due_date', 'paid_date', 'status',
            'status_display', 'payment_terms', 'notes', 'days_overdue',
            'is_overdue', 'amount_paid', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class ExpenseSerializer(serializers.ModelSerializer):
    """Expense serializer"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)
    receipt_url = serializers.CharField(source='receipt.url', read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'project', 'project_name', 'category', 'category_display',
            'amount', 'date', 'description', 'vendor', 'receipt',
            'receipt_url', 'receipt_number', 'tax_deductible', 'approved',
            'approved_by', 'approved_by_name', 'approval_date', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'approved', 'approved_by', 'approval_date', 'created_at', 'updated_at'
        ]


class RevenueSerializer(serializers.ModelSerializer):
    """Revenue serializer"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    revenue_type_display = serializers.CharField(source='get_revenue_type_display', read_only=True)
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)

    class Meta:
        model = Revenue
        fields = [
            'id', 'project', 'project_name', 'revenue_type', 'revenue_type_display',
            'amount', 'date', 'client_name', 'invoice', 'invoice_number',
            'payment_method', 'payment_method_display', 'transaction_id', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class BudgetSerializer(serializers.ModelSerializer):
    """Budget serializer"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    budget_type_display = serializers.CharField(source='get_budget_type_display', read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    remaining_amount = serializers.ReadOnlyField()
    utilization_percentage = serializers.ReadOnlyField()
    is_over_budget = serializers.ReadOnlyField()
    status_color = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = [
            'id', 'name', 'budget_type', 'budget_type_display', 'project',
            'project_name', 'department', 'allocated_amount', 'spent_amount',
            'remaining_amount', 'utilization_percentage', 'is_over_budget',
            'status_color', 'start_date', 'end_date', 'currency', 'owner',
            'owner_name', 'notes', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_status_color(self, obj):
        """Return color based on budget utilization"""
        utilization = obj.utilization_percentage
        if utilization >= 100:
            return 'red'
        elif utilization >= 80:
            return 'orange'
        elif utilization >= 60:
            return 'yellow'
        else:
            return 'green'


class FinancialReportSerializer(serializers.ModelSerializer):
    """Financial report serializer"""
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    generated_by_name = serializers.CharField(source='generated_by.get_full_name', read_only=True)
    file_url = serializers.CharField(source='file_path', read_only=True)

    class Meta:
        model = FinancialReport
        fields = [
            'id', 'report_type', 'report_type_display', 'title', 'description',
            'start_date', 'end_date', 'generated_date', 'generated_by',
            'generated_by_name', 'file_path', 'file_url', 'data_summary',
            'is_public', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'generated_by', 'generated_date', 'created_at', 'updated_at'
        ]


class FinanceAnalyticsSerializer(serializers.Serializer):
    """Finance analytics dashboard serializer"""
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
    profit_margin = serializers.DecimalField(max_digits=5, decimal_places=2)
    total_invoices = serializers.IntegerField()
    unpaid_invoices = serializers.IntegerField()
    overdue_invoices = serializers.IntegerField()
    total_outstanding = serializers.DecimalField(max_digits=12, decimal_places=2)
    payroll_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    operational_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    
    # Monthly trends
    monthly_revenue = serializers.ListField(child=serializers.DecimalField(max_digits=12, decimal_places=2))
    monthly_expenses = serializers.ListField(child=serializers.DecimalField(max_digits=12, decimal_places=2))
    monthly_profit = serializers.ListField(child=serializers.DecimalField(max_digits=12, decimal_places=2))
    
    # Top categories
    expense_categories = serializers.ListField(child=serializers.DictField())
    revenue_by_type = serializers.ListField(child=serializers.DictField())
    
    # Budget status
    budget_utilization = serializers.ListField(child=serializers.DictField())


class ProjectBurnRateSerializer(serializers.Serializer):
    """Project burn rate analytics"""
    project_id = serializers.IntegerField()
    project_name = serializers.CharField()
    total_budget = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    remaining_budget = serializers.DecimalField(max_digits=12, decimal_places=2)
    burn_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    daily_burn_rate = serializers.DecimalField(max_digits=8, decimal_places=2)
    days_remaining = serializers.IntegerField()
    projected_end_date = serializers.DateField()
    status = serializers.CharField()  # 'ON_TRACK', 'AT_RISK', 'OVER_BUDGET'