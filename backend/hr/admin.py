from django.contrib import admin
from .models import (
    Department, Employee, Skill, EmployeeSkill,
    LeaveRequest, PerformanceReview, Attendance
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'budget', 'parent_department', 'created_at']
    list_filter = ['parent_department']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'employee_count']
    list_filter = ['category']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']
    
    def employee_count(self, obj):
        return obj.employees.count()
    employee_count.short_description = 'Employees'


class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'department', 'position', 'is_active', 'hire_date']
    list_filter = ['department', 'position', 'is_active', 'hire_date']
    search_fields = [
        'employee_id', 'user__username', 'user__first_name',
        'user__last_name', 'department', 'position'
    ]
    ordering = ['employee_id']
    inlines = [EmployeeSkillInline]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'leave_type', 'start_date', 'end_date',
        'days_requested', 'status', 'approved_by', 'created_at'
    ]
    list_filter = ['leave_type', 'status', 'start_date', 'created_at']
    search_fields = [
        'employee__user__username', 'employee__user__first_name',
        'employee__user__last_name', 'reason'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'approval_date']


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'review_type', 'review_date', 'reviewer',
        'overall_rating', 'average_rating', 'created_at'
    ]
    list_filter = ['review_type', 'overall_rating', 'review_date']
    search_fields = [
        'employee__user__username', 'employee__user__first_name',
        'employee__user__last_name', 'reviewer__username',
        'strengths', 'areas_for_improvement'
    ]
    ordering = ['-review_date']
    readonly_fields = ['created_at', 'updated_at', 'average_rating']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'date', 'status', 'check_in', 'check_out',
        'hours_worked', 'overtime_hours', 'created_at'
    ]
    list_filter = ['status', 'date']
    search_fields = [
        'employee__user__username', 'employee__user__first_name',
        'employee__user__last_name', 'notes'
    ]
    ordering = ['-date', 'employee']
    readonly_fields = ['created_at', 'updated_at', 'hours_worked']
    date_hierarchy = 'date'


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = [
        'employee', 'skill', 'proficiency', 'years_experience',
        'last_used', 'created_at'
    ]
    list_filter = ['proficiency', 'skill__category']
    search_fields = [
        'employee__user__username', 'employee__user__first_name',
        'employee__user__last_name', 'skill__name'
    ]
    ordering = ['-proficiency', '-years_experience']
    readonly_fields = ['created_at', 'updated_at']