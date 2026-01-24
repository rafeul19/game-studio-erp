from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from erp_projects.models import Project

class Payroll(models.Model):
    """Employee payroll records"""
    PAYROLL_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    ]

    employee = models.ForeignKey(
        'hr.Employee',
        on_delete=models.CASCADE,
        related_name='payroll_records'
    )
    month = models.DateField(help_text="Payroll month (first day of month)")
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    overtime_rate = models.DecimalField(max_digits=5, decimal_places=2, default=1.5)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PAYROLL_STATUS,
        default='PENDING'
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('BANK_TRANSFER', 'Bank Transfer'),
            ('CHECK', 'Check'),
            ('CASH', 'Cash'),
            ('DIGITAL', 'Digital Wallet'),
        ],
        default='BANK_TRANSFER'
    )
    bank_account = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'month')
        ordering = ['-month', 'employee']
        verbose_name = 'Payroll'
        verbose_name_plural = 'Payroll Records'

    def __str__(self):
        return f"{self.employee.user.username} - {self.month.strftime('%B %Y')}"

    def calculate_net_salary(self):
        """Calculate net salary including overtime"""
        gross = self.base_salary + self.bonuses
        overtime_pay = self.overtime_hours * (self.base_salary / 160) * self.overtime_rate
        total_gross = gross + overtime_pay
        return total_gross - self.deductions

    def save(self, *args, **kwargs):
        self.net_salary = self.calculate_net_salary()
        super().save(*args, **kwargs)


class Invoice(models.Model):
    """Project invoices and client billing"""
    INVOICE_STATUS = [
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    invoice_number = models.CharField(max_length=50, unique=True)
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField(blank=True)
    client_address = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.0000)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=INVOICE_STATUS,
        default='DRAFT'
    )
    payment_terms = models.CharField(
        max_length=100,
        default='NET 30',
        help_text="Payment terms (e.g., NET 30, Due on Receipt)"
    )
    notes = models.TextField(
        blank=True,
        help_text="Additional notes or payment instructions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date']
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        return f"INV-{self.invoice_number}"

    def save(self, *args, **kwargs):
        self.tax_amount = self.amount * (self.tax_rate / 100)
        self.total_amount = self.amount + self.tax_amount
        super().save(*args, **kwargs)

    @property
    def days_overdue(self):
        """Calculate days overdue"""
        if self.status in ['PAID', 'CANCELLED']:
            return 0
        return (timezone.now().date() - self.due_date).days

    @property
    def is_overdue(self):
        """Check if invoice is overdue"""
        return self.status not in ['PAID', 'CANCELLED'] and self.due_date < timezone.now().date()


class Expense(models.Model):
    """Project and operational expenses"""
    EXPENSE_CATEGORIES = [
        ('SOFTWARE', 'Software & Licenses'),
        ('HARDWARE', 'Hardware & Equipment'),
        ('OFFICE', 'Office Supplies'),
        ('MARKETING', 'Marketing & Advertising'),
        ('TRAVEL', 'Travel & Entertainment'),
        ('TRAINING', 'Training & Education'),
        ('UTILITIES', 'Utilities'),
        ('RENT', 'Rent & Lease'),
        ('INSURANCE', 'Insurance'),
        ('LEGAL', 'Legal & Professional'),
        ('BANK_FEES', 'Bank Fees'),
        ('OTHER', 'Other'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='expenses',
        help_text="Leave blank for company-wide expenses"
    )
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    description = models.TextField()
    vendor = models.CharField(max_length=200, help_text="Company or individual paid to")
    receipt = models.FileField(
        upload_to='receipts/%Y/%m/%d/',
        null=True,
        blank=True
    )
    receipt_number = models.CharField(max_length=100, blank=True)
    tax_deductible = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_expenses'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'

    def __str__(self):
        return f"{self.category}: {self.amount} - {self.date}"


class Revenue(models.Model):
    """Revenue tracking and client payments"""
    REVENUE_TYPES = [
        ('PROJECT_PAYMENT', 'Project Payment'),
        ('RETAINER', 'Retainer Fee'),
        ('CONSULTING', 'Consulting Income'),
        ('LICENSING', 'Licensing Revenue'),
        ('TRAINING', 'Training Revenue'),
        ('SUPPORT', 'Support Contract'),
        ('OTHER', 'Other Revenue'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='revenue'
    )
    revenue_type = models.CharField(max_length=50, choices=REVENUE_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateField()
    client_name = models.CharField(max_length=200)
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments'
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('BANK_TRANSFER', 'Bank Transfer'),
            ('CHECK', 'Check'),
            ('CASH', 'Cash'),
            ('CREDIT_CARD', 'Credit Card'),
            ('PAYPAL', 'PayPal'),
            ('CRYPTO', 'Cryptocurrency'),
            ('OTHER', 'Other'),
        ]
    )
    transaction_id = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Revenue'
        verbose_name_plural = 'Revenue Records'

    def __str__(self):
        return f"{self.client_name}: {self.amount} - {self.date}"


class Budget(models.Model):
    """Project and department budgets"""
    BUDGET_TYPES = [
        ('PROJECT', 'Project Budget'),
        ('DEPARTMENT', 'Department Budget'),
        ('OPERATIONAL', 'Operational Budget'),
        ('MARKETING', 'Marketing Budget'),
        ('CAPITAL', 'Capital Expenditure'),
    ]

    name = models.CharField(max_length=200)
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPES)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='budgets'
    )
    department = models.CharField(max_length=100, blank=True)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    currency = models.CharField(max_length=3, default='USD')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_budgets'
    )
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        return f"{self.name} - {self.allocated_amount} {self.currency}"

    @property
    def remaining_amount(self):
        """Calculate remaining budget"""
        return self.allocated_amount - self.spent_amount

    @property
    def utilization_percentage(self):
        """Calculate budget utilization"""
        if self.allocated_amount == 0:
            return 0
        return (self.spent_amount / self.allocated_amount) * 100

    @property
    def is_over_budget(self):
        """Check if budget is exceeded"""
        return self.spent_amount > self.allocated_amount


class FinancialReport(models.Model):
    """Generated financial reports"""
    REPORT_TYPES = [
        ('P&L', 'Profit & Loss'),
        ('BALANCE_SHEET', 'Balance Sheet'),
        ('CASH_FLOW', 'Cash Flow Statement'),
        ('PROJECT_REPORT', 'Project Financial Report'),
        ('DEPARTMENT_REPORT', 'Department Financial Report'),
        ('EXPENSE_REPORT', 'Expense Report'),
        ('REVENUE_REPORT', 'Revenue Report'),
    ]

    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_date = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='generated_reports'
    )
    file_path = models.CharField(max_length=500, blank=True)
    data_summary = models.JSONField(default=dict, help_text="Report summary data in JSON format")
    is_public = models.BooleanField(default=False, help_text="Whether report is accessible to all users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-generated_date']
        verbose_name = 'Financial Report'
        verbose_name_plural = 'Financial Reports'

    def __str__(self):
        return f"{self.report_type}: {self.title} ({self.generated_date.strftime('%Y-%m-%d')})"