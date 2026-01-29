from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Employee, Skill, EmployeeSkill, LeaveRequest, 
    PerformanceReview, Attendance, Department
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Basic user information for HR purposes"""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name()


class DepartmentSerializer(serializers.ModelSerializer):
    """Department serializer for HR management"""
    manager_name = serializers.CharField(source='manager.user.get_full_name', read_only=True)
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'description', 'manager', 'manager_name', 
            'budget', 'parent_department', 'employee_count', 'created_at', 'updated_at'
        ]

    def get_employee_count(self, obj):
        return Employee.objects.filter(department=obj.name, is_active=True).count()


class SkillSerializer(serializers.ModelSerializer):
    """Skill serializer"""
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'description', 'employee_count', 'created_at']

    def get_employee_count(self, obj):
        return EmployeeSkill.objects.filter(skill=obj).count()


class EmployeeSkillSerializer(serializers.ModelSerializer):
    """Employee skill relationship serializer"""
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    skill_category = serializers.CharField(source='skill.category', read_only=True)
    proficiency_display = serializers.CharField(source='get_proficiency_display', read_only=True)

    class Meta:
        model = EmployeeSkill
        fields = [
            'id', 'skill', 'skill_name', 'skill_category', 'proficiency', 
            'proficiency_display', 'years_experience', 'certifications', 
            'last_used', 'created_at', 'updated_at'
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    """Employee profile serializer"""
    user_info = UserSerializer(source='user', read_only=True)
    skills = EmployeeSkillSerializer(many=True, read_only=True)
    employment_status = serializers.ReadOnlyField()
    years_of_service = serializers.ReadOnlyField()
    department_name = serializers.CharField(source='department', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'user_info', 'employee_id', 'department', 'department_name',
            'position', 'hire_date', 'salary', 'phone', 'address', 
            'emergency_contact', 'emergency_phone', 'is_active', 
            'termination_date', 'termination_reason', 'employment_status',
            'years_of_service', 'skills', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class LeaveRequestSerializer(serializers.ModelSerializer):
    """Leave request serializer"""
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    leave_type_display = serializers.CharField(source='get_leave_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    days_requested = serializers.ReadOnlyField()
    approved_by_name = serializers.CharField(source='approved_by.get_full_name', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_name', 'employee_id', 'leave_type',
            'leave_type_display', 'start_date', 'end_date', 'days_requested',
            'reason', 'status', 'status_display', 'approved_by', 
            'approved_by_name', 'approval_date', 'approval_comments',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['employee', 'approved_by', 'approval_date', 'created_at', 'updated_at']


class PerformanceReviewSerializer(serializers.ModelSerializer):
    """Performance review serializer"""
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    review_type_display = serializers.CharField(source='get_review_type_display', read_only=True)
    overall_rating_display = serializers.CharField(source='get_overall_rating_display', read_only=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = PerformanceReview
        fields = [
            'id', 'employee', 'employee_name', 'review_type', 'review_type_display',
            'review_date', 'reviewer', 'reviewer_name', 'overall_rating',
            'overall_rating_display', 'strengths', 'areas_for_improvement',
            'goals', 'technical_skills_rating', 'communication_rating',
            'teamwork_rating', 'problem_solving_rating', 'leadership_rating',
            'average_rating', 'comments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class AttendanceSerializer(serializers.ModelSerializer):
    """Attendance record serializer"""
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    hours_worked = serializers.ReadOnlyField()

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_name', 'employee_id', 'date',
            'check_in', 'check_out', 'status', 'status_display',
            'notes', 'overtime_hours', 'hours_worked', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class EmployeeDetailSerializer(EmployeeSerializer):
    """Detailed employee information for HR management"""
    leave_requests = LeaveRequestSerializer(many=True, read_only=True)
    performance_reviews = PerformanceReviewSerializer(many=True, read_only=True)
    attendance_records = AttendanceSerializer(many=True, read_only=True)

    class Meta(EmployeeSerializer.Meta):
        fields = EmployeeSerializer.Meta.fields + [
            'leave_requests', 'performance_reviews', 'attendance_records'
        ]


class HREmployeeSkillMatrixSerializer(serializers.Serializer):
    """Serializer for skills matrix visualization"""
    skill_name = serializers.CharField()
    skill_category = serializers.CharField()
    employees = serializers.ListField(
        child=serializers.DictField()
    )
    
    def to_representation(self, instance):
        # Custom implementation for skills matrix
        return instance