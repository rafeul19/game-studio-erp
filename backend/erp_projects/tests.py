from decimal import Decimal
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import timedelta, date

from erp_projects.models import Project, Task, Sprint
from accounts.models import User

User = get_user_model()


class ProjectModelTest(TestCase):
    """Test Project model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='MANAGER'
        )
        self.project = Project.objects.create(
            name='Test Game Project',
            description='A test game development project',
            owner=self.user,
            total_budget=Decimal('100000.00'),
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=90)
        )
    
    def test_project_creation(self):
        """Test project creation"""
        self.assertEqual(self.project.name, 'Test Game Project')
        self.assertEqual(self.project.owner, self.user)
        self.assertEqual(self.project.total_budget, Decimal('100000.00'))
        self.assertEqual(self.project.status, 'PLANNING')
    
    def test_project_str_representation(self):
        """Test project string representation"""
        self.assertEqual(str(self.project), 'Test Game Project')
    
    def test_project_progress_percentage(self):
        """Test project progress calculation"""
        # Initially should be 0%
        self.assertEqual(self.project.progress_percentage(), 0)
        
        # Add some tasks
        Task.objects.create(
            title='Task 1',
            description='First task',
            project=self.project,
            status='DONE',
            story_points=5
        )
        Task.objects.create(
            title='Task 2',
            description='Second task',
            project=self.project,
            status='TODO',
            story_points=3
        )
        
        # Should be (5 / 8) * 100 = 62.5%
        self.assertAlmostEqual(self.project.progress_percentage(), 62.5)
    
    def test_project_budget_remaining(self):
        """Test budget calculation"""
        self.assertEqual(self.project.budget_remaining(), Decimal('100000.00'))
        # Will test with expenses later


class TaskModelTest(TestCase):
    """Test Task model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='DEVELOPER'
        )
        self.project = Project.objects.create(
            name='Test Project',
            owner=self.user,
            total_budget=Decimal('50000.00')
        )
        self.task = Task.objects.create(
            title='Test Task',
            description='A test task',
            project=self.project,
            assigned_to=self.user,
            status='TODO',
            priority='HIGH',
            story_points=8
        )
    
    def test_task_creation(self):
        """Test task creation"""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.assigned_to, self.user)
        self.assertEqual(self.task.status, 'TODO')
        self.assertEqual(self.task.priority, 'HIGH')
        self.assertEqual(self.task.story_points, 8)
    
    def test_task_str_representation(self):
        """Test task string representation"""
        self.assertEqual(str(self.task), 'Test Task')
    
    def test_task_is_overdue(self):
        """Test overdue task detection"""
        # Future due date should not be overdue
        self.task.due_date = timezone.now().date() + timedelta(days=7)
        self.task.save()
        self.assertFalse(self.task.is_overdue())
        
        # Past due date should be overdue
        self.task.due_date = timezone.now().date() - timedelta(days=1)
        self.task.save()
        self.assertTrue(self.task.is_overdue())


class SprintModelTest(TestCase):
    """Test Sprint model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='MANAGER'
        )
        self.project = Project.objects.create(
            name='Test Project',
            owner=self.user,
            total_budget=Decimal('50000.00')
        )
        self.sprint = Sprint.objects.create(
            name='Sprint 1',
            project=self.project,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=14)
        )
    
    def test_sprint_creation(self):
        """Test sprint creation"""
        self.assertEqual(self.sprint.name, 'Sprint 1')
        self.assertEqual(self.sprint.project, self.project)
        self.assertEqual(self.sprint.status, 'PLANNED')
    
    def test_sprint_str_representation(self):
        """Test sprint string representation"""
        self.assertEqual(str(self.sprint), 'Test Project - Sprint 1')
    
    def test_sprint_velocity_calculation(self):
        """Test sprint velocity calculation"""
        # Add tasks to sprint
        Task.objects.create(
            title='Done Task 1',
            project=self.project,
            sprint=self.sprint,
            status='DONE',
            story_points=5
        )
        Task.objects.create(
            title='Done Task 2',
            project=self.project,
            sprint=self.sprint,
            status='DONE',
            story_points=3
        )
        Task.objects.create(
            title='Todo Task',
            project=self.project,
            sprint=self.sprint,
            status='TODO',
            story_points=8
        )
        
        # Velocity should only count completed tasks IN A COMPLETED SPRINT
        self.sprint.status = Sprint.COMPLETED
        self.sprint.save()
        self.assertEqual(self.sprint.velocity(), 8)
    
    def test_sprint_total_story_points(self):
        """Test total story points calculation"""
        Task.objects.create(
            title='Task 1',
            project=self.project,
            sprint=self.sprint,
            story_points=5
        )
        Task.objects.create(
            title='Task 2',
            project=self.project,
            sprint=self.sprint,
            story_points=3
        )
        
        self.assertEqual(self.sprint.total_story_points(), 8)


class ProjectAPITest(APITestCase):
    """Test Project API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='MANAGER'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_project(self):
        """Test project creation API"""
        data = {
            'name': 'API Test Project',
            'description': 'Testing project creation via API',
            'total_budget': '75000.00',
            'start_date': timezone.now().date().isoformat(),
            'end_date': (timezone.now().date() + timedelta(days=60)).isoformat()
        }
        
        response = self.client.post('/api/projects/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        project = Project.objects.get(id=response.data['id'])
        self.assertEqual(project.name, 'API Test Project')
        self.assertEqual(project.owner, self.user)
    
    def test_my_projects_endpoint(self):
        """Test my projects endpoint"""
        # Create some projects
        Project.objects.create(name='Project 1', owner=self.user)
        Project.objects.create(name='Project 2', owner=self.user)
        
        response = self.client.get('/api/projects/my/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_project_progress_endpoint(self):
        """Test project progress endpoint"""
        project = Project.objects.create(name='Test Project', owner=self.user)
        
        response = self.client.get(f'/api/projects/{project.id}/progress/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('progress_percentage', response.data)
        self.assertIn('tasks_by_status', response.data)


class TaskAPITest(APITestCase):
    """Test Task API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='DEVELOPER'
        )
        self.manager = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='managerpass123',
            role='MANAGER'
        )
        self.project = Project.objects.create(
            name='Test Project',
            owner=self.manager,
            total_budget=Decimal('50000.00')
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_task(self):
        """Test task creation API"""
        data = {
            'title': 'API Test Task',
            'description': 'Testing task creation via API',
            'project': self.project.id,
            'priority': 'HIGH',
            'story_points': 5
        }
        
        response = self.client.post('/api/tasks/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        task = Task.objects.get(id=response.data['id'])
        self.assertEqual(task.title, 'API Test Task')
        self.assertEqual(task.project, self.project)
    
    def test_my_tasks_endpoint(self):
        """Test my tasks endpoint"""
        # Create some tasks
        Task.objects.create(
            title='Task 1',
            project=self.project,
            assigned_to=self.user,
            status='TODO'
        )
        Task.objects.create(
            title='Task 2',
            project=self.project,
            assigned_to=self.user,
            status='IN_PROGRESS'
        )
        
        response = self.client.get('/api/tasks/my/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_update_task_status(self):
        """Test task status update"""
        task = Task.objects.create(
            title='Test Task',
            project=self.project,
            assigned_to=self.user,
            status='TODO'
        )
        
        data = {'status': 'IN_PROGRESS'}
        response = self.client.patch(f'/api/tasks/{task.id}/status/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        task.refresh_from_db()
        self.assertEqual(task.status, 'IN_PROGRESS')


class SprintAPITest(APITestCase):
    """Test Sprint API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='MANAGER'
        )
        self.project = Project.objects.create(
            name='Test Project',
            owner=self.user,
            total_budget=Decimal('50000.00')
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_sprint(self):
        """Test sprint creation API"""
        data = {
            'name': 'API Test Sprint',
            'project': self.project.id,
            'start_date': timezone.now().date().isoformat(),
            'end_date': (timezone.now().date() + timedelta(days=14)).isoformat()
        }
        
        response = self.client.post('/api/sprints/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        sprint = Sprint.objects.get(id=response.data['id'])
        self.assertEqual(sprint.name, 'API Test Sprint')
        self.assertEqual(sprint.project, self.project)
    
    def test_sprint_progress_endpoint(self):
        """Test sprint progress endpoint"""
        sprint = Sprint.objects.create(
            name='Test Sprint',
            project=self.project,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=14)
        )
        
        response = self.client.get(f'/api/sprints/{sprint.id}/progress/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('velocity', response.data)
        self.assertIn('total_points', response.data)


class AIEstimationTest(TestCase):
    """Test AI estimation services"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='MANAGER'
        )
        self.project = Project.objects.create(
            name='Test Project',
            owner=self.user,
            total_budget=Decimal('50000.00')
        )
    
    def test_story_point_suggestion(self):
        """Test story point suggestion"""
        from erp_projects.ai_service import AIEstimationService
        
        # Simple task
        points = AIEstimationService.suggest_story_points(
            'Simple UI fix',
            'Fix button color'
        )
        self.assertGreater(points, 0)
        self.assertLessEqual(points, 21)
        
        # Complex task should have more or equal points (dependent on ML, but should be >0)
        complex_points = AIEstimationService.suggest_story_points(
            'Implement authentication system',
            'Create full user authentication with JWT tokens, password reset, and email verification'
        )
        self.assertGreater(complex_points, 0)
    
    def test_sprint_risk_prediction(self):
        """Test sprint risk prediction"""
        from erp_projects.ai_service import AIEstimationService
        
        sprint = Sprint.objects.create(
            name='Test Sprint',
            project=self.project,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=14)
        )
        
        risk = AIEstimationService.predict_sprint_risk(sprint)
        self.assertIn(risk, ['LOW', 'MEDIUM', 'HIGH'])
    
    def test_sprint_capacity_calculation(self):
        """Test sprint capacity calculation"""
        from erp_projects.ai_service import AIEstimationService
        
        capacity = AIEstimationService.calculate_sprint_capacity(self.project)
        self.assertIsInstance(capacity, int)
        self.assertGreater(capacity, 0)