from django.contrib import admin
from django.utils import timezone
from .models import (
    Payroll, Invoice, Expense, Revenue, 
    Budget, FinancialReport
)


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'month', 'base_salary', 'bonuses', 'net_salary',
        'status', 'paid_date'
    ]
    list_filter = ['status', 'payment_method', 'month']
    search_fields = [
        'employee__user__username', 'employee__user__first_name',
        'employee__user__last_name', 'employee__employee_id'
    ]
    ordering = ['-month', 'employee']
    readonly_fields = ['created_at', 'updated_at', 'net_salary']
    date_hierarchy = 'month'


class ExpenseInline(admin.TabularInline):
    model = Expense
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number', 'client_name', 'project', 'amount',
        'total_amount', 'status', 'issue_date', 'due_date'
    ]
    list_filter = ['status', 'issue_date', 'due_date']
    search_fields = [
        'invoice_number', 'client_name', 'client_email',
        'project__name'
    ]
    ordering = ['-issue_date']
    readonly_fields = ['created_at', 'updated_at', 'tax_amount', 'total_amount']
    date_hierarchy = 'issue_date'


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = [
        'vendor', 'category', 'amount', 'date', 'project',
        'approved', 'approval_date'
    ]
    list_filter = ['category', 'approved', 'date']
    search_fields = [
        'vendor', 'description', 'receipt_number',
        'project__name'
    ]
    ordering = ['-date']
    readonly_fields = ['created_at', 'updated_at', 'approval_date']
    date_hierarchy = 'date'
    
    actions = ['mark_as_approved']
    
    def mark_as_approved(self, request, queryset):
        """Mark selected expenses as approved"""
        for expense in queryset:
            expense.approved = True
            expense.approved_by = request.user
            expense.approval_date = timezone.now()
            expense.save()
        
        self.message_user(
            request, 
            f'{queryset.count()} expenses were marked as approved.',
            level='success'
        )
    mark_as_approved.short_description = 'Mark selected expenses as approved'


@admin.register(Revenue)
class RevenueAdmin(admin.ModelAdmin):
    list_display = [
        'client_name', 'revenue_type', 'amount', 'date',
        'project', 'invoice', 'payment_method'
    ]
    list_filter = ['revenue_type', 'payment_method', 'date']
    search_fields = [
        'client_name', 'transaction_id', 'project__name',
        'invoice__invoice_number'
    ]
    ordering = ['-date']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'budget_type', 'allocated_amount', 'spent_amount',
        'remaining_amount', 'utilization_percentage', 'is_active'
    ]
    list_filter = ['budget_type', 'is_active', 'start_date']
    search_fields = ['name', 'department', 'project__name']
    ordering = ['-created_at']
    readonly_fields = [
        'created_at', 'updated_at', 'spent_amount',
        'remaining_amount', 'utilization_percentage'
    ]
    date_hierarchy = 'start_date'
    
    def utilization_percentage(self, obj):
        percentage = obj.utilization_percentage
        if percentage >= 100:
            return f'<span style="color: red;">{percentage:.1f}%</span>'
        elif percentage >= 80:
            return f'<span style="color: orange;">{percentage:.1f}%</span>'
        else:
            return f'<span style="color: green;">{percentage:.1f}%</span>'
    utilization_percentage.allow_tags = True


@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'report_type', 'generated_date', 'generated_by',
        'start_date', 'end_date', 'is_public'
    ]
    list_filter = ['report_type', 'is_public', 'generated_date']
    search_fields = ['title', 'description']
    ordering = ['-generated_date']
    readonly_fields = [
        'generated_by', 'generated_date', 'created_at', 'updated_at',
        'data_summary'
    ]
    date_hierarchy = 'generated_date'