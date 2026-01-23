from django.utils import timezone
from .models import Sprint, Task
from accounts.models import User

class AIEstimationService:
    @staticmethod
    def predict_sprint_risk(sprint):
        """
        Predicts if a sprint is at risk of not completing.
        - Risk if total points > average velocity of past 3 sprints.
        - Risk if end date is too close and many tasks are TODO.
        """
        total_points = sprint.total_story_points()
        past_sprints = Sprint.objects.filter(
            project=sprint.project,
            status=Sprint.COMPLETED
        ).order_by('-end_date')[:3]
        
        if not past_sprints:
            return "MEDIUM (No historical data)"
        
        avg_velocity = sum(s.velocity() for s in past_sprints) / len(past_sprints)
        
        if total_points > avg_velocity * 1.2:
            return "HIGH (Over capacity)"
        
        return "LOW"

    @staticmethod
    def suggest_story_points(task_title, task_description):
        """
        Simple heuristic-based suggestion.
        In a real app, this would use an LLM or ML classifier.
        """
        complexity = 1
        words = (task_title + " " + task_description).lower().split()
        
        complex_keywords = ['implement', 'integrate', 'refactor', 'database', 'auth']
        medium_keywords = ['update', 'fix', 'ui', 'style']
        
        for word in words:
            if word in complex_keywords:
                complexity += 3
            elif word in medium_keywords:
                complexity += 1
                
        return min(complexity, 13) # Fibonacci-ish cap

    @staticmethod
    def detect_asset_reuse(project, task_title):
        """
        Detects potential asset/code reuse from existing tasks in the project.
        """
        existing_tasks = Task.objects.filter(project=project)
        keywords = set(task_title.lower().split())
        
        matches = []
        for task in existing_tasks:
            task_keywords = set(task.title.lower().split())
            common = keywords.intersection(task_keywords)
            if len(common) >= 2: # At least 2 common keywords
                matches.append(task.title)
        
        return matches[:3]

    @staticmethod
    def calculate_sprint_capacity(project):
        """
        Calculates suggested capacity for the next sprint based on average velocity.
        """
        past_sprints = Sprint.objects.filter(
            project=project,
            status=Sprint.COMPLETED
        ).order_by('-end_date')[:3]
        
        if not past_sprints:
            return 20 # Default for first sprint
            
        avg_velocity = sum(s.velocity() for s in past_sprints) / len(past_sprints)
        return int(avg_velocity)
