from django.utils import timezone
from .models import Sprint, Task
from accounts.models import User
from .ml.train_models import get_story_point_prediction, get_sprint_risk_prediction, get_asset_recommendations

class AIEstimationService:
    @staticmethod
    def predict_sprint_risk(sprint):
        """
        ML-based sprint risk prediction with fallback to heuristics.
        """
        try:
            # Try ML prediction first
            ml_prediction = get_sprint_risk_prediction(sprint)
            if ml_prediction:
                return ml_prediction
        except Exception:
            pass
        
        # Fallback to heuristic
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
    def suggest_story_points(task_title, task_description, project_id=None):
        """
        ML-based story point suggestion with fallback to heuristics.
        """
        try:
            # Try ML prediction first
            ml_prediction = get_story_point_prediction(task_title, task_description, project_id)
            if ml_prediction:
                return ml_prediction
        except Exception:
            pass
        
        # Fallback to heuristic
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
        ML-based asset reuse detection with fallback to keyword matching.
        """
        from assets.models import Asset
        
        try:
            # Try ML recommendations first
            ml_recommendations = get_asset_recommendations(project.id, task_title)
            if ml_recommendations:
                return ml_recommendations
        except Exception:
            pass
        
        # Fallback to keyword matching
        keywords = set(task_title.lower().replace(',', ' ').split())
        if len(keywords) < 2:
            return []

        # Check existing Assets
        asset_matches = Asset.objects.filter(project=project)
        reuse_suggestions = []
        
        for asset in asset_matches:
            asset_text = (asset.name + " " + asset.tags).lower()
            asset_keywords = set(asset_text.replace(',', ' ').split())
            common = keywords.intersection(asset_keywords)
            if len(common) >= 1: # Even 1 strong tag match is good for assets
                reuse_suggestions.append({
                    "type": "ASSET",
                    "title": asset.name,
                    "id": asset.id,
                    "tags": asset.tags
                })

        # Check existing Tasks (previous logic)
        existing_tasks = Task.objects.filter(project=project)
        for task in existing_tasks:
            task_keywords = set(task.title.lower().split())
            common = keywords.intersection(task_keywords)
            if len(common) >= 2:
                reuse_suggestions.append({
                    "type": "TASK",
                    "title": task.title,
                    "id": task.id
                })
        
        return reuse_suggestions[:5]

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
