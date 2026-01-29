from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hr.models import Employee, Department, Skill, EmployeeSkill
from erp_projects.models import Project, Task, Sprint, WorkLog
from finance.models import Invoice, Expense, Budget, Revenue
from assets.models import Asset
from bugs.models import Bug
from django.utils import timezone
from decimal import Decimal
import datetime
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with sample data for game studio ERP'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Create Departments
        depts_data = [
            {'name': 'Engineering', 'description': 'Software development and systems'},
            {'name': 'Art & UI', 'description': 'Visual assets and user interface'},
            {'name': 'Game Design', 'description': 'Mechanics and level design'},
            {'name': 'QA', 'description': 'Quality assurance and testing'},
            {'name': 'Management', 'description': 'Project and studio management'},
        ]
        
        departments = {}
        for d in depts_data:
            dept, created = Department.objects.get_or_create(name=d['name'], defaults={'description': d['description']})
            departments[d['name']] = dept

        # 2. Create Skills
        skills_data = [
            {'name': 'Unreal Engine 5', 'category': 'ENGINE'},
            {'name': 'Unity', 'category': 'ENGINE'},
            {'name': 'C++', 'category': 'PROGRAMMING'},
            {'name': 'C#', 'category': 'PROGRAMMING'},
            {'name': 'Python', 'category': 'PROGRAMMING'},
            {'name': 'Blender', 'category': 'ART'},
            {'name': 'Maya', 'category': 'ART'},
            {'name': 'Photoshop', 'category': 'ART'},
        ]
        
        skills = []
        for s in skills_data:
            skill, created = Skill.objects.get_or_create(name=s['name'], defaults={'category': s['category']})
            skills.append(skill)

        # 3. Create Users and Employees
        users_data = [
            {'username': 'john.dev', 'first_name': 'John', 'last_name': 'Doe', 'role': 'DEVELOPER', 'dept': 'Engineering'},
            {'username': 'jane.art', 'first_name': 'Jane', 'last_name': 'Smith', 'role': 'ARTIST', 'dept': 'Art & UI'},
            {'username': 'bob.mgr', 'first_name': 'Bob', 'last_name': 'Wilson', 'role': 'MANAGER', 'dept': 'Management'},
            {'username': 'alice.qa', 'first_name': 'Alice', 'last_name': 'Brown', 'role': 'QA', 'dept': 'QA'},
        ]

        for u in users_data:
            user, created = User.objects.get_or_create(
                username=u['username'],
                defaults={
                    'email': f"{u['username']}@example.com",
                    'first_name': u['first_name'],
                    'last_name': u['last_name'],
                    'role': u['role'],
                    'is_staff': True if u['role'] in ['ADMIN', 'MANAGER'] else False
                }
            )
            if created:
                user.set_password('admin123')
                user.save()
                
            emp, e_created = Employee.objects.get_or_create(
                user=user,
                defaults={
                    'employee_id': f"EMP{random.randint(1000, 9999)}",
                    'department': u['dept'],
                    'position': u['role'].capitalize(),
                    'hire_date': timezone.now().date() - datetime.timedelta(days=random.randint(100, 500)),
                    'salary': Decimal(random.randint(50000, 120000)),
                }
            )
            
            if e_created:
                selected_skills = random.sample(skills, min(len(skills), 3))
                for skill in selected_skills:
                    EmployeeSkill.objects.get_or_create(employee=emp, skill=skill, defaults={'proficiency': random.randint(3, 5), 'years_experience': Decimal(random.randint(1, 10))})

        # 4. Create Projects
        projects_data = [
            {'name': 'Cyber Quest 2077', 'description': 'Open world RPG'},
            {'name': 'Space Raiders', 'description': 'Mobile arcade shooter'},
            {'name': 'Medieval Mayhem', 'description': 'Multiplayer strategy'},
            {'name': 'Z-Hunter', 'description': 'Survival horror'},
            {'name': 'Racing Master', 'description': 'Simulation racing'},
        ]
        
        mgr_user = User.objects.filter(role='MANAGER').first()
        
        project_objs = []
        for p in projects_data:
            proj, created = Project.objects.get_or_create(
                name=p['name'],
                defaults={
                    'description': p['description'],
                    'owner': mgr_user,
                    'budget_type': 'FIXED',
                    'total_budget': Decimal(random.randint(100000, 500000))
                }
            )
            project_objs.append(proj)

        # 5. Create Sprints and Tasks (Need 10+ completed sprints and 10+ completed tasks)
        dev_user = User.objects.filter(role='DEVELOPER').first()
        for proj in project_objs:
            for s_idx in range(3): # 3 sprints per project = 15 sprints total
                sprint, _ = Sprint.objects.get_or_create(
                    name=f"Sprint {s_idx+1} - {proj.name}",
                    project=proj,
                    defaults={
                        'start_date': timezone.now().date() - datetime.timedelta(days=30*(s_idx+1)),
                        'end_date': timezone.now().date() - datetime.timedelta(days=30*s_idx + 1),
                        'status': 'COMPLETED'
                    }
                )
                
                # Tasks for each sprint
                for t_idx in range(5):
                    Task.objects.get_or_create(
                        title=f"Task {t_idx+1} in {sprint.name}",
                        project=proj,
                        defaults={
                            'description': f"Requirement for {t_idx+1}",
                            'sprint': sprint,
                            'status': 'DONE',
                            'priority': random.choice(['LOW', 'MEDIUM', 'HIGH']),
                            'assigned_to': dev_user,
                            'story_points': random.choice([1, 2, 3, 5, 8])
                        }
                    )

        # 6. Create Assets (Need 5+)
        artist_user = User.objects.filter(role='ARTIST').first()
        asset_names = ['Hero Model', 'Villain Model', 'Boss Texture', 'Forest Environment', 'City Skybox', 'Sword SFX', 'Menu Music']
        for i, name in enumerate(asset_names):
            Asset.objects.get_or_create(
                name=name,
                defaults={
                    'project': random.choice(project_objs),
                    'asset_type': '3D' if 'Model' in name else 'AUDIO' if 'SFX' in name else 'OTHER',
                    'owner': artist_user,
                    'tags': 'game,asset,2024'
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded enough data for ML training!'))
