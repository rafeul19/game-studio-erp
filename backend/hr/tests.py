from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from decimal import Decimal
from datetime import timedelta, date

from hr.models import Employee, Skill, EmployeeSkill, LeaveRequest, PerformanceReview, Attendance, Department
from erp_projects.models import Project

User = get_user_model()


class EmployeeModelTest(TestCase):
    """Test Employee model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id='EMP001',
            department='Engineering',
            position='Senior Developer',
            hire_date=timezone.now().date() - timedelta(days=365),
            salary=Decimal('75000.00')
        )
    
    def test_employee_creation(self):
        """Test employee creation"""
        self.assertEqual(self.employee.employee_id, 'EMP001')
        self.assertEqual(self.employee.department, 'Engineering')
        self.assertEqual(self.employee.position, 'Senior Developer')
        self.assertEqual(self.employee.salary, Decimal('75000.00'))
        self.assertTrue(self.employee.is_active)
    
    def test_employee_str_representation(self):
        """Test employee string representation"""
        expected = "EMP001 - John Doe"
        self.assertEqual(str(self.employee), expected)
    
    def test_years_of_service(self):
        """Test years of service calculation"""
        years = self.employee.years_of_service
        self.assertAlmostEqual(years, 1.0, places=1)
    
    def test_employment_status(self):
        """Test employment status calculation"""
        # Active employee
        self.assertEqual(self.employee.employment_status, 'Active')
        
        # Inactive employee
        self.employee.is_active = False
        self.employee.save()
        self.assertEqual(self.employee.employment_status, 'Terminated')


class SkillModelTest(TestCase):
    """Test Skill model functionality"""
    
    def test_skill_creation(self):
        """Test skill creation"""
        skill = Skill.objects.create(
            name='Python',
            category='PROGRAMMING',
            description='Python programming language'
        )
        
        self.assertEqual(skill.name, 'Python')
        self.assertEqual(skill.category, 'PROGRAMMING')
        self.assertEqual(str(skill), '[PROGRAMMING] Python')
    
    def test_skill_category_display(self):
        """Test skill category display"""
        skill = Skill.objects.create(
            name='Unity',
            category='ENGINE'
        )
        
        self.assertEqual(skill.get_category_display(), 'Game Engine')


class EmployeeSkillTest(TestCase):
    """Test EmployeeSkill model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id='EMP001',
            department='Engineering',
            position='Developer',
            hire_date=timezone.now().date(),
            salary=Decimal('60000.00')
        )
        self.skill = Skill.objects.create(
            name='Python',
            category='PROGRAMMING'
        )
        self.employee_skill = EmployeeSkill.objects.create(
            employee=self.employee,
            skill=self.skill,
            proficiency=3,
            years_experience=2.5
        )
    
    def test_employee_skill_creation(self):
        """Test employee skill creation"""
        self.assertEqual(self.employee_skill.employee, self.employee)
        self.assertEqual(self.employee_skill.skill, self.skill)
        self.assertEqual(self.employee_skill.proficiency, 3)
        self.assertEqual(self.employee_skill.years_experience, Decimal('2.5'))
    
    def test_employee_skill_unique_constraint(self):
        """Test unique constraint on employee-skill combination"""
        with self.assertRaises(Exception):
            EmployeeSkill.objects.create(
                employee=self.employee,
                skill=self.skill,
                proficiency=4
            )


class LeaveRequestTest(TestCase):
    """Test LeaveRequest model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.manager_user = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='managerpass123'
        )
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id='EMP001',
            department='Engineering',
            position='Developer',
            hire_date=timezone.now().date(),
            salary=Decimal('60000.00')
        )
        self.leave_request = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type='VACATION',
            start_date=timezone.now().date() + timedelta(days=10),
            end_date=timezone.now().date() + timedelta(days=14),
            reason='Family vacation'
        )
    
    def test_leave_request_creation(self):
        """Test leave request creation"""
        self.assertEqual(self.leave_request.employee, self.employee)
        self.assertEqual(self.leave_request.leave_type, 'VACATION')
        self.assertEqual(self.leave_request.status, 'PENDING')
        self.assertEqual(self.leave_request.days_requested, 5)
    
    def test_leave_request_approval(self):
        """Test leave request approval"""
        self.leave_request.status = 'APPROVED'
        self.leave_request.approved_by = self.manager_user
        self.leave_request.approval_date = timezone.now()
        self.leave_request.save()
        
        self.assertEqual(self.leave_request.status, 'APPROVED')
        self.assertEqual(self.leave_request.approved_by, self.manager_user)


class PerformanceReviewTest(TestCase):
    """Test PerformanceReview model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.reviewer = User.objects.create_user(
            username='reviewer',
            email='reviewer@example.com',
            password='reviewerpass123'
        )
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id='EMP001',
            department='Engineering',
            position='Developer',
            hire_date=timezone.now().date(),
            salary=Decimal('60000.00')
        )
        self.review = PerformanceReview.objects.create(
            employee=self.employee,
            review_type='QUARTERLY',
            review_date=timezone.now().date(),
            reviewer=self.reviewer,
            overall_rating=3,
            strengths='Great problem solver',
            areas_for_improvement='Communication skills',
            goals='Improve documentation',
            technical_skills_rating=4,
            communication_rating=2,
            teamwork_rating=3,
            problem_solving_rating=4
        )
    
    def test_performance_review_creation(self):
        """Test performance review creation"""
        self.assertEqual(self.review.employee, self.employee)
        self.assertEqual(self.review.review_type, 'QUARTERLY')
        self.assertEqual(self.review.overall_rating, 3)
    
    def test_average_rating_calculation(self):
        """Test average rating calculation"""
        expected_average = (3 + 4 + 2 + 3 + 4) / 5  # 3.2
        self.assertAlmostEqual(self.review.average_rating, expected_average)


class AttendanceTest(TestCase):
    """Test Attendance model functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id='EMP001',
            department='Engineering',
            position='Developer',
            hire_date=timezone.now().date(),
            salary=Decimal('60000.00')
        )
        self.attendance = Attendance.objects.create(
            employee=self.employee,
            date=timezone.now().date(),
            check_in='09:00:00',
            check_out='17:30:00',
            status='PRESENT'
        )
    
    def test_attendance_creation(self):
        """Test attendance creation"""
        self.assertEqual(self.attendance.employee, self.employee)
        self.assertEqual(self.attendance.status, 'PRESENT')
        self.assertEqual(self.attendance.overtime_hours, 0)
    
    def test_hours_worked_calculation(self):
        """Test hours worked calculation"""
        # 8.5 hours + overtime = total hours
        self.assertGreater(self.attendance.hours_worked, 8)
    
    def test_attendance_unique_constraint(self):
        """Test unique constraint on employee-date"""
        with self.assertRaises(Exception):
            Attendance.objects.create(
                employee=self.employee,
                date=timezone.now().date(),
                status='PRESENT'
            )


class DepartmentTest(TestCase):
    """Test Department model functionality"""
    
    def test_department_creation(self):
        """Test department creation"""
        manager_user = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='managerpass123'
        )
        manager_employee = Employee.objects.create(
            user=manager_user,
            employee_id='MGR001',
            department='Engineering',
            position='Engineering Manager',
            hire_date=timezone.now().date(),
            salary=Decimal('90000.00')
        )
        
        department = Department.objects.create(
            name='Engineering',
            description='Software development team',
            manager=manager_employee,
            budget=Decimal('500000.00')
        )
        
        self.assertEqual(department.name, 'Engineering')
        self.assertEqual(department.manager, manager_employee)
        self.assertEqual(department.budget, Decimal('500000.00'))


class EmployeeAPITest(APITestCase):
    """Test Employee API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='MANAGER'
        )
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id='EMP001',
            department='Engineering',
            position='Developer',
            hire_date=timezone.now().date(),
            salary=Decimal('60000.00')
        )
        self.client.force_authenticate(user=self.user)
    
    def test_employee_list(self):
        """Test employee list endpoint"""
        response = self.client.get('/api/hr/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_employee_detail(self):
        """Test employee detail endpoint"""
        response = self.client.get(f'/api/hr/employees/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('employee_id', response.data)
        self.assertIn('user_info', response.data)
    
    def test_employee_analytics(self):
        """Test employee analytics endpoint"""
        response = self.client.get('/api/hr/employees/analytics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('overview', response.data)
        self.assertIn('department_distribution', response.data)
    
    def test_add_employee_skill(self):
        """Test adding skill to employee"""
        skill = Skill.objects.create(
            name='Django',
            category='PROGRAMMING'
        )
        
        data = {
            'skill_id': skill.id,
            'proficiency': 4,
            'years_experience': 3.0,
            'certifications': 'Django Certification'
        }
        
        response = self.client.post(
            f'/api/hr/employees/{self.employee.id}/add_skill/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK or status.HTTP_201_CREATED)
        
        self.assertTrue(
            EmployeeSkill.objects.filter(
                employee=self.employee,
                skill=skill
            ).exists()
        )


class LeaveRequestAPITest(APITestCase):
    """Test LeaveRequest API endpoints"""
    
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
        self.employee = Employee.objects.create(
            user=self.user,
            employee_id='EMP001',
            department='Engineering',
            position='Developer',
            hire_date=timezone.now().date(),
            salary=Decimal('60000.00')
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_leave_request(self):
        """Test leave request creation"""
        data = {
            'leave_type': 'SICK',
            'start_date': (timezone.now().date() + timedelta(days=5)).isoformat(),
            'end_date': (timezone.now().date() + timedelta(days=6)).isoformat(),
            'reason': 'Medical appointment'
        }
        
        response = self.client.post('/api/hr/leave-requests/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        leave_request = LeaveRequest.objects.get(id=response.data['id'])
        self.assertEqual(leave_request.employee, self.employee)
        self.assertEqual(leave_request.leave_type, 'SICK')
    
    def test_approve_leave_request(self):
        """Test leave request approval"""
        self.client.force_authenticate(user=self.manager)
        
        leave_request = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type='VACATION',
            start_date=timezone.now().date() + timedelta(days=10),
            end_date=timezone.now().date() + timedelta(days=12),
            reason='Vacation'
        )
        
        response = self.client.post(
            f'/api/hr/leave-requests/{leave_request.id}/approve/',
            {'comments': 'Approved'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        leave_request.refresh_from_db()
        self.assertEqual(leave_request.status, 'APPROVED')
        self.assertEqual(leave_request.approved_by, self.manager)


class SkillAPITest(APITestCase):
    """Test Skill API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='MANAGER'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_skill_list(self):
        """Test skill list endpoint"""
        Skill.objects.create(name='Python', category='PROGRAMMING')
        Skill.objects.create(name='Unity', category='ENGINE')
        
        response = self.client.get('/api/hr/skills/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_skill_creation(self):
        """Test skill creation"""
        data = {
            'name': 'React',
            'category': 'PROGRAMMING',
            'description': 'React.js framework'
        }
        
        response = self.client.post('/api/hr/skills/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        skill = Skill.objects.get(id=response.data['id'])
        self.assertEqual(skill.name, 'React')
        self.assertEqual(skill.category, 'PROGRAMMING')