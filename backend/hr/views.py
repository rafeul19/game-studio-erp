from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, Avg, Count
from django.contrib.auth import get_user_model
from .models import (
    Employee, Skill, EmployeeSkill, LeaveRequest, 
    PerformanceReview, Attendance, Department
)
from .serializers import (
    EmployeeSerializer, EmployeeDetailSerializer, SkillSerializer,
    EmployeeSkillSerializer, LeaveRequestSerializer, 
    PerformanceReviewSerializer, AttendanceSerializer,
    DepartmentSerializer, HREmployeeSkillMatrixSerializer
)

User = get_user_model()


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing departments"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent_department']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet for managing employees"""
    queryset = Employee.objects.select_related('user').prefetch_related('skills__skill')
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'position', 'is_active']
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name',
        'employee_id', 'department', 'position'
    ]
    ordering_fields = ['employee_id', 'hire_date', 'created_at']
    ordering = ['employee_id']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        return EmployeeSerializer

    @action(detail=False, methods=['get'])
    def skills_matrix(self, request):
        """Generate skills matrix for all employees"""
        skills = Skill.objects.prefetch_related('employees__employee__user')
        
        matrix_data = []
        for skill in skills:
            employees_with_skill = []
            for emp_skill in skill.employees.all():
                if emp_skill.employee.is_active:
                    employees_with_skill.append({
                        'employee_id': emp_skill.employee.employee_id,
                        'employee_name': emp_skill.employee.user.get_full_name(),
                        'proficiency': emp_skill.proficiency,
                        'proficiency_display': emp_skill.get_proficiency_display(),
                        'years_experience': emp_skill.years_experience,
                        'department': emp_skill.employee.department,
                    })
            
            matrix_data.append({
                'skill_name': skill.name,
                'skill_category': skill.category,
                'skill_category_display': skill.get_category_display(),
                'employees': employees_with_skill
            })
        
        return Response(matrix_data)

    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """HR analytics dashboard data"""
        total_employees = Employee.objects.filter(is_active=True).count()
        total_departments = Department.objects.count()
        
        # Department distribution
        dept_stats = Employee.objects.filter(is_active=True).values('department').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Skills coverage
        skill_coverage = Skill.objects.annotate(
            employee_count=Count('employees')
        ).order_by('-employee_count')[:10]
        
        # Recent leave requests
        recent_leaves = LeaveRequest.objects.select_related(
            'employee__user'
        ).order_by('-created_at')[:5]
        
        # Upcoming reviews
        upcoming_reviews = PerformanceReview.objects.filter(
            review_date__gte=timezone.now().date()
        ).select_related('employee__user', 'reviewer').order_by('review_date')[:5]
        
        # Attendance summary (last 30 days)
        thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)
        attendance_summary = Attendance.objects.filter(
            date__gte=thirty_days_ago
        ).values('status').annotate(count=Count('id'))
        
        return Response({
            'overview': {
                'total_employees': total_employees,
                'total_departments': total_departments,
                'active_employees': total_employees,
            },
            'department_distribution': list(dept_stats),
            'skill_coverage': [
                {
                    'skill_name': skill.name,
                    'employee_count': skill.employee_count
                } for skill in skill_coverage
            ],
            'recent_leave_requests': LeaveRequestSerializer(
                recent_leaves, many=True
            ).data,
            'upcoming_reviews': PerformanceReviewSerializer(
                upcoming_reviews, many=True
            ).data,
            'attendance_summary': list(attendance_summary),
        })

    @action(detail=True, methods=['post'])
    def add_skill(self, request, pk=None):
        """Add or update a skill for an employee"""
        employee = self.get_object()
        
        skill_id = request.data.get('skill_id')
        proficiency = request.data.get('proficiency')
        years_experience = request.data.get('years_experience')
        certifications = request.data.get('certifications', '')
        
        try:
            skill = Skill.objects.get(id=skill_id)
            emp_skill, created = EmployeeSkill.objects.update_or_create(
                employee=employee,
                skill=skill,
                defaults={
                    'proficiency': proficiency,
                    'years_experience': years_experience,
                    'certifications': certifications,
                    'last_used': timezone.now().date()
                }
            )
            
            serializer = EmployeeSkillSerializer(emp_skill)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except Skill.DoesNotExist:
            return Response(
                {'error': 'Skill not found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class SkillViewSet(viewsets.ModelViewSet):
    """ViewSet for managing skills"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'category', 'created_at']
    ordering = ['category', 'name']


class LeaveRequestViewSet(viewsets.ModelViewSet):
    """ViewSet for managing leave requests"""
    queryset = LeaveRequest.objects.select_related('employee__user', 'approved_by')
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'leave_type', 'status']
    search_fields = [
        'employee__user__username', 'employee__user__first_name',
        'employee__user__last_name', 'reason'
    ]
    ordering_fields = ['created_at', 'start_date', 'end_date']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user.employee_profile)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a leave request"""
        leave_request = self.get_object()
        
        if leave_request.status != 'PENDING':
            return Response(
                {'error': 'Leave request is not pending'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leave_request.status = 'APPROVED'
        leave_request.approved_by = request.user
        leave_request.approval_date = timezone.now()
        leave_request.approval_comments = request.data.get('comments', '')
        leave_request.save()
        
        return Response(LeaveRequestSerializer(leave_request).data)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a leave request"""
        leave_request = self.get_object()
        
        if leave_request.status != 'PENDING':
            return Response(
                {'error': 'Leave request is not pending'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        leave_request.status = 'REJECTED'
        leave_request.approved_by = request.user
        leave_request.approval_date = timezone.now()
        leave_request.approval_comments = request.data.get('comments', '')
        leave_request.save()
        
        return Response(LeaveRequestSerializer(leave_request).data)


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for managing performance reviews"""
    queryset = PerformanceReview.objects.select_related('employee__user', 'reviewer')
    serializer_class = PerformanceReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'reviewer', 'review_type', 'overall_rating']
    search_fields = [
        'employee__user__username', 'employee__user__first_name',
        'employee__user__last_name', 'strengths', 'areas_for_improvement'
    ]
    ordering_fields = ['review_date', 'created_at']
    ordering = ['-review_date']

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class AttendanceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing attendance records"""
    queryset = Attendance.objects.select_related('employee__user')
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['employee', 'status']
    search_fields = [
        'employee__user__username', 'employee__user__first_name',
        'employee__user__last_name', 'notes'
    ]
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get attendance summary for a date range"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'Both start_date and end_date are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        attendance_summary = Attendance.objects.filter(
            date__range=[start_date, end_date]
        ).values('employee__employee_id', 'employee__user__username').annotate(
            total_days=Count('id'),
            present_days=Count('id', filter=Q(status='PRESENT')),
            absent_days=Count('id', filter=Q(status='ABSENT')),
            late_days=Count('id', filter=Q(status='LATE')),
            total_overtime=Avg('overtime_hours')
        ).order_by('employee__employee_id')
        
        return Response(list(attendance_summary))