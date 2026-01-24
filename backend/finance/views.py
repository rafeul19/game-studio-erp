from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Sum, Avg, Count, F, ExpressionWrapper, DecimalField
from django.http import HttpResponse
from django.db import transaction
import csv
from datetime import timedelta
from decimal import Decimal
from .models import (
    Payroll, Invoice, Expense, Revenue, 
    Budget, FinancialReport
)
from .serializers import (
    PayrollSerializer, InvoiceSerializer, ExpenseSerializer,
    RevenueSerializer, BudgetSerializer, FinancialReportSerializer,
    FinanceAnalyticsSerializer, ProjectBurnRateSerializer
)


class PayrollViewSet(viewsets.ModelViewSet):
    """ViewSet for managing payroll"""
    queryset = Payroll.objects.select_related('employee__user').all()
    serializer_class = PayrollSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'status', 'payment_method']
    search_fields = [
        'employee__user__username', 'employee__user__first_name',
        'employee__user__last_name', 'employee__employee_id'
    ]
    ordering_fields = ['month', 'created_at']
    ordering = ['-month']

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve payroll for payment"""
        payroll = self.get_object()
        
        if payroll.status != 'PENDING':
            return Response(
                {'error': 'Payroll is not in pending status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payroll.status = 'APPROVED'
        payroll.save()
        
        return Response(PayrollSerializer(payroll).data)

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark payroll as paid"""
        payroll = self.get_object()
        paid_date = request.data.get('paid_date')
        
        if payroll.status != 'APPROVED':
            return Response(
                {'error': 'Payroll must be approved before marking as paid'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payroll.status = 'PAID'
        payroll.paid_date = paid_date or timezone.now().date()
        payroll.save()
        
        return Response(PayrollSerializer(payroll).data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get payroll summary for a period"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'Both start_date and end_date are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        summary = Payroll.objects.filter(
            month__range=[start_date, end_date]
        ).aggregate(
            total_payroll=Sum('net_salary'),
            total_base_salary=Sum('base_salary'),
            total_bonuses=Sum('bonuses'),
            total_deductions=Sum('deductions'),
            total_overtime_hours=Sum('overtime_hours'),
            employee_count=Count('employee', distinct=True)
        )
        
        return Response(summary)


class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing invoices"""
    queryset = Invoice.objects.select_related('project').all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'status', 'client_name']
    search_fields = [
        'invoice_number', 'client_name', 'client_email', 'project__name'
    ]
    ordering_fields = ['issue_date', 'due_date', 'amount']
    ordering = ['-issue_date']

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark invoice as paid"""
        invoice = self.get_object()
        paid_date = request.data.get('paid_date')
        
        invoice.status = 'PAID'
        invoice.paid_date = paid_date or timezone.now().date()
        invoice.save()
        
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Mark invoice as sent to client"""
        invoice = self.get_object()
        
        if invoice.status == 'DRAFT':
            invoice.status = 'SENT'
            invoice.save()
        
        return Response(InvoiceSerializer(invoice).data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue invoices"""
        overdue_invoices = Invoice.objects.filter(
            status__in=['SENT'],
            due_date__lt=timezone.now().date()
        ).order_by('due_date')
        
        serializer = self.get_serializer(overdue_invoices, many=True)
        return Response(serializer.data)


class ExpenseViewSet(viewsets.ModelViewSet):
    """ViewSet for managing expenses"""
    queryset = Expense.objects.select_related('project', 'approved_by').all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'category', 'approved']
    search_fields = [
        'description', 'vendor', 'receipt_number', 'project__name'
    ]
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']

    def perform_create(self, serializer):
        """Auto-approve for small expenses"""
        expense_data = serializer.validated_data
        amount = expense_data.get('amount', 0)
        
        # Auto-approve expenses under $100
        if amount <= 100:
            expense = serializer.save(approved=True, approved_by=self.request.user)
            expense.approval_date = timezone.now()
            expense.save()
        else:
            serializer.save()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve expense"""
        expense = self.get_object()
        
        expense.approved = True
        expense.approved_by = request.user
        expense.approval_date = timezone.now()
        expense.save()
        
        return Response(ExpenseSerializer(expense).data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get expense summary by category"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = Expense.objects.filter(approved=True)
        
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        summary = queryset.values('category').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        return Response(list(summary))


class RevenueViewSet(viewsets.ModelViewSet):
    """ViewSet for managing revenue"""
    queryset = Revenue.objects.select_related('project', 'invoice').all()
    serializer_class = RevenueSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'revenue_type', 'client_name']
    search_fields = [
        'client_name', 'transaction_id', 'project__name', 'invoice__invoice_number'
    ]
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get revenue summary by type"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        queryset = Revenue.objects.all()
        
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        
        summary = queryset.values('revenue_type').annotate(
            total_amount=Sum('amount'),
            count=Count('id')
        ).order_by('-total_amount')
        
        return Response(list(summary))


class BudgetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing budgets"""
    queryset = Budget.objects.select_related('project', 'owner').all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['project', 'budget_type', 'department', 'is_active']
    search_fields = ['name', 'description', 'department']
    ordering_fields = ['created_at', 'allocated_amount', 'utilization_percentage']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def update_spent(self, request, pk=None):
        """Update spent amount for budget"""
        budget = self.get_object()
        amount = request.data.get('amount', 0)
        
        budget.spent_amount = F('spent_amount') + amount
        budget.save(update_fields=['spent_amount'])
        
        budget.refresh_from_db()
        return Response(BudgetSerializer(budget).data)

    @action(detail=False, methods=['get'])
    def utilization(self, request):
        """Get budget utilization report"""
        active_budgets = Budget.objects.filter(is_active=True)
        
        utilization_data = []
        for budget in active_budgets:
            utilization_data.append({
                'budget_id': budget.id,
                'budget_name': budget.name,
                'allocated': budget.allocated_amount,
                'spent': budget.spent_amount,
                'remaining': budget.remaining_amount,
                'utilization_percent': budget.utilization_percentage,
                'status': 'OVER_BUDGET' if budget.is_over_budget else 
                         'AT_RISK' if budget.utilization_percentage >= 80 else
                         'ON_TRACK'
            })
        
        return Response(utilization_data)


class FinancialReportViewSet(viewsets.ModelViewSet):
    """ViewSet for managing financial reports"""
    queryset = FinancialReport.objects.select_related('generated_by').all()
    serializer_class = FinancialReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['report_type', 'is_public']
    search_fields = ['title', 'description']
    ordering_fields = ['generated_date', 'report_type']
    ordering = ['-generated_date']

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get financial analytics dashboard data"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Default to last 12 months if not provided
        if not end_date:
            end_date = timezone.now().date()
        if not start_date:
            start_date = end_date - timedelta(days=365)
        
        # Calculate totals
        revenue_data = Revenue.objects.filter(
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))
        
        expense_data = Expense.objects.filter(
            approved=True,
            date__range=[start_date, end_date]
        ).aggregate(total=Sum('amount'))
        
        payroll_data = Payroll.objects.filter(
            month__range=[start_date, end_date]
        ).aggregate(total=Sum('net_salary'))
        
        total_revenue = revenue_data['total'] or 0
        total_expenses = (expense_data['total'] or 0) + (payroll_data['total'] or 0)
        net_profit = total_revenue - total_expenses
        profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Invoice statistics
        invoice_stats = Invoice.objects.filter(
            issue_date__range=[start_date, end_date]
        ).aggregate(
            total=Count('id'),
            unpaid=Count('id', filter=Q(status__in=['DRAFT', 'SENT'])),
            overdue=Count('id', filter=Q(status='SENT', due_date__lt=timezone.now().date())),
            outstanding=Sum('total_amount', filter=Q(status__in=['DRAFT', 'SENT']))
        )
        
        # Monthly trends (simplified - in real implementation, would use proper date trunc)
        monthly_data = []
        for i in range(12):
            month_start = end_date.replace(day=1) - timedelta(days=30*i)
            month_end = month_start.replace(day=28) + timedelta(days=4)  # Handle month end
            
            month_revenue = Revenue.objects.filter(
                date__range=[month_start, month_end]
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            month_expenses = Expense.objects.filter(
                approved=True,
                date__range=[month_start, month_end]
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            monthly_data.append({
                'month': month_start.strftime('%Y-%m'),
                'revenue': float(month_revenue),
                'expenses': float(month_expenses),
                'profit': float(month_revenue - month_expenses)
            })
        
        return Response({
            'total_revenue': total_revenue,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'profit_margin': profit_margin,
            'total_invoices': invoice_stats['total'] or 0,
            'unpaid_invoices': invoice_stats['unpaid'] or 0,
            'overdue_invoices': invoice_stats['overdue'] or 0,
            'total_outstanding': invoice_stats['outstanding'] or 0,
            'payroll_expense': payroll_data['total'] or 0,
            'operational_expenses': expense_data['total'] or 0,
            'monthly_trends': monthly_data,
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        })

    @action(detail=False, methods=['get'])
    def project_burn_rate(self, request):
        """Calculate project burn rates"""
        projects_with_expenses = Expense.objects.filter(
            project__isnull=False,
            approved=True
        ).select_related('project').values('project')
        
        burn_rate_data = []
        for project_data in projects_with_expenses:
            project = project_data['project']
            
            # Get project budget and expenses
            total_budget = project.total_budget or 0
            expenses = Expense.objects.filter(project=project, approved=True)
            total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0
            
            if total_budget > 0:
                burn_rate = (total_spent / total_budget) * 100
                
                # Calculate daily burn rate and days remaining
                first_expense = expenses.order_by('date').first()
                if first_expense:
                    days_active = (timezone.now().date() - first_expense.date).days
                    daily_burn_rate = total_spent / days_active if days_active > 0 else 0
                    days_remaining = int((total_budget - total_spent) / daily_burn_rate) if daily_burn_rate > 0 else 999
                else:
                    daily_burn_rate = 0
                    days_remaining = 999
                
                projected_end_date = timezone.now().date() + timedelta(days=days_remaining)
                
                burn_rate_data.append({
                    'project_id': project.id,
                    'project_name': project.name,
                    'total_budget': total_budget,
                    'total_spent': total_spent,
                    'remaining_budget': total_budget - total_spent,
                    'burn_rate': burn_rate,
                    'daily_burn_rate': daily_burn_rate,
                    'days_remaining': days_remaining,
                    'projected_end_date': projected_end_date,
                    'status': 'OVER_BUDGET' if burn_rate >= 100 else
                            'AT_RISK' if burn_rate >= 80 else 'ON_TRACK'
                })
        
        return Response(burn_rate_data)

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        """Export financial report as CSV"""
        report = self.get_object()
        
        if report.report_type == 'P&L':
            # Generate P&L report CSV
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{report.title}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Category', 'Amount', 'Date'])
            
            # Add revenue data
            revenues = Revenue.objects.filter(date__range=[report.start_date, report.end_date])
            for revenue in revenues:
                writer.writerow(['Revenue', revenue.amount, revenue.date])
            
            # Add expense data
            expenses = Expense.objects.filter(
                approved=True,
                date__range=[report.start_date, report.end_date]
            )
            for expense in expenses:
                writer.writerow([expense.category, expense.amount, expense.date])
            
            return response
        
        return Response(
            {'error': 'Export not available for this report type'},
            status=status.HTTP_400_BAD_REQUEST
        )