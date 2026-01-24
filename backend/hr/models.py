from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

class Employee(models.Model):
    """Extended user profile for HR management"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    employee_id = models.CharField(max_length=20, unique=True, help_text="Unique employee identifier")
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, help_text="Annual salary")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True, help_text="Whether employee is currently active")
    termination_date = models.DateField(null=True, blank=True)
    termination_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"

    @property
    def years_of_service(self):
        """Calculate years of service"""
        end_date = self.termination_date if self.termination_date else timezone.now().date()
        return (end_date - self.hire_date).days / 365.25

    @property
    def employment_status(self):
        """Get current employment status"""
        if not self.is_active:
            return "Terminated"
        elif self.termination_date:
            return "Notice Period"
        else:
            return "Active"


class Skill(models.Model):
    """Skills that can be associated with employees"""
    SKILL_CATEGORIES = [
        ('ENGINE', 'Game Engine'),
        ('PROGRAMMING', 'Programming Language'),
        ('ART', 'Art Tool'),
        ('AUDIO', 'Audio Tool'),
        ('DESIGN', 'Design Tool'),
        ('SOFT_SKILL', 'Soft Skill'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'

    def __str__(self):
        return f"[{self.get_category_display()}] {self.name}"


class EmployeeSkill(models.Model):
    """Many-to-many relationship between employees and skills with proficiency"""
    PROFICIENCY_LEVELS = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Expert'),
        (5, 'Master'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='skills'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    proficiency = models.IntegerField(
        choices=PROFICIENCY_LEVELS,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    years_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0)],
        help_text="Years of experience with this skill"
    )
    certifications = models.TextField(
        blank=True,
        help_text="Relevant certifications or qualifications"
    )
    last_used = models.DateField(
        null=True,
        blank=True,
        help_text="When this skill was last used in a project"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'skill')
        ordering = ['-proficiency', '-years_experience']
        verbose_name = 'Employee Skill'
        verbose_name_plural = 'Employee Skills'

    def __str__(self):
        return f"{self.employee.user.username} - {self.skill.name} ({self.get_proficiency_display()})"


class LeaveRequest(models.Model):
    """Employee leave requests"""
    LEAVE_TYPES = [
        ('SICK', 'Sick Leave'),
        ('VACATION', 'Vacation'),
        ('PERSONAL', 'Personal Leave'),
        ('MATERNITY', 'Maternity Leave'),
        ('PATERNITY', 'Paternity Leave'),
        ('UNPAID', 'Unpaid Leave'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves'
    )
    approval_date = models.DateTimeField(null=True, blank=True)
    approval_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Leave Request'
        verbose_name_plural = 'Leave Requests'

    def __str__(self):
        return f"{self.employee.user.username} - {self.get_leave_type_display()} ({self.start_date} to {self.end_date})"

    @property
    def days_requested(self):
        """Calculate total days requested"""
        return (self.end_date - self.start_date).days + 1

    def clean(self):
        """Validate leave request dates"""
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date")


class PerformanceReview(models.Model):
    """Employee performance reviews"""
    REVIEW_TYPES = [
        ('QUARTERLY', 'Quarterly Review'),
        ('ANNUAL', 'Annual Review'),
        ('PROJECT', 'Project-Based Review'),
        ('PROBATION', 'Probation Review'),
        ('ADHOC', 'Ad-hoc Review'),
    ]

    RATING_CHOICES = [
        (1, 'Needs Improvement'),
        (2, 'Meets Expectations'),
        (3, 'Exceeds Expectations'),
        (4, 'Outstanding'),
        (5, 'Exceptional'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='performance_reviews'
    )
    review_type = models.CharField(max_length=20, choices=REVIEW_TYPES)
    review_date = models.DateField()
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='conducted_reviews'
    )
    overall_rating = models.IntegerField(choices=RATING_CHOICES)
    strengths = models.TextField(help_text="Employee's strengths and achievements")
    areas_for_improvement = models.TextField(help_text="Areas that need improvement")
    goals = models.TextField(help_text="Goals for next review period")
    technical_skills_rating = models.IntegerField(choices=RATING_CHOICES)
    communication_rating = models.IntegerField(choices=RATING_CHOICES)
    teamwork_rating = models.IntegerField(choices=RATING_CHOICES)
    problem_solving_rating = models.IntegerField(choices=RATING_CHOICES)
    leadership_rating = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True,
        help_text="N/A for non-leadership roles"
    )
    comments = models.TextField(blank=True, help_text="Additional comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-review_date']
        verbose_name = 'Performance Review'
        verbose_name_plural = 'Performance Reviews'

    def __str__(self):
        return f"{self.employee.user.username} - {self.get_review_type_display()} ({self.review_date})"

    @property
    def average_rating(self):
        """Calculate average of all ratings"""
        ratings = [
            self.overall_rating,
            self.technical_skills_rating,
            self.communication_rating,
            self.teamwork_rating,
            self.problem_solving_rating,
        ]
        if self.leadership_rating:
            ratings.append(self.leadership_rating)
        return sum(ratings) / len(ratings)


class Attendance(models.Model):
    """Employee attendance records"""
    ATTENDANCE_STATUS = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
        ('HALF_DAY', 'Half Day'),
        ('WORK_FROM_HOME', 'Work From Home'),
        ('ON_LEAVE', 'On Leave'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS)
    notes = models.TextField(blank=True, help_text="Reason for absence/late/etc.")
    overtime_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        help_text="Overtime hours worked"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date', 'employee']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'

    def __str__(self):
        return f"{self.employee.user.username} - {self.date} ({self.get_status_display()})"

    @property
    def hours_worked(self):
        """Calculate hours worked for the day"""
        if self.check_in and self.check_out:
            # Simple calculation - in real implementation, handle overnight shifts
            start = timezone.datetime.combine(self.date, self.check_in)
            end = timezone.datetime.combine(self.date, self.check_out)
            duration = end - start
            hours = duration.total_seconds() / 3600
            return hours + float(self.overtime_hours)
        return 0


class Department(models.Model):
    """Company departments"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
        help_text="Department manager"
    )
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Annual budget for department"
    )
    parent_department = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sub_departments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name