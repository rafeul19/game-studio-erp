from django.db import models
from accounts.models import User


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    members = models.ManyToManyField(
        User,
        blank=True,
        related_name='projects'
    )
    budget_type = models.CharField(max_length=20, choices=[('FIXED', 'Fixed Budget'), ('T&M', 'Time & Materials')], default='FIXED')
    total_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('PLANNING', 'Planning'), ('ACTIVE', 'Active'), ('ON_HOLD', 'On Hold'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')],
        default='PLANNING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def progress_percentage(self):
        from django.db.models import Sum
        total_points = self.tasks.aggregate(Sum('story_points'))['story_points__sum'] or 0
        if total_points == 0:
            return 0
        done_points = self.tasks.filter(status='DONE').aggregate(Sum('story_points'))['story_points__sum'] or 0
        return (done_points / total_points) * 100

    def budget_remaining(self):
        return self.total_budget


class Sprint(models.Model):
    PLANNED = 'PLANNED'
    ACTIVE = 'ACTIVE'
    COMPLETED = 'COMPLETED'

    STATUS_CHOICES = [
        (PLANNED, 'Planned'),
        (ACTIVE, 'Active'),
        (COMPLETED, 'Completed'),
    ]

    name = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='sprints'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PLANNED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.name} - {self.name}"

    def progress_percentage(self):
        total = self.tasks.count()
        if total == 0:
            return 0
        done = self.tasks.filter(status='DONE').count()
        return int((done / total) * 100)

    def total_story_points(self):
        return sum(task.story_points for task in self.tasks.all())

    def velocity(self):
        if self.status != Sprint.COMPLETED:
            return 0
        return sum(task.story_points for task in self.tasks.filter(status='DONE'))


class Task(models.Model):
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    REVIEW = 'REVIEW'
    DONE = 'DONE'

    STATUS_CHOICES = [
        (TODO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (REVIEW, 'Review'),
        (DONE, 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=TODO
    )
    priority = models.CharField(
        max_length=20,
        choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('URGENT', 'Urgent')],
        default='MEDIUM'
    )
    due_date = models.DateField(null=True, blank=True)
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    story_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_overdue(self):
        if self.due_date and self.status != self.DONE:
            from django.utils import timezone
            return self.due_date < timezone.now().date()
        return False

    def __str__(self):
        return self.title


class WorkLog(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='worklogs'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='worklogs'
    )
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    is_billable = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.task.title} - {self.hours} hrs"
