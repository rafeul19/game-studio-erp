import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.preprocessing import StandardScaler
from django.db.models import Q, Count, Avg
import joblib
import os
import numpy as np
from decimal import Decimal

from erp_projects.models import Task, Sprint
from assets.models import Asset


def train_story_point_model():
    """
    Train a machine learning model to suggest story points based on historical data.
    """
    # Collect historical task data
    completed_tasks = Task.objects.filter(
        status='DONE',
        story_points__gt=0
    ).select_related('project', 'assigned_to').annotate(
        project_task_count=Count('project__tasks'),
        assignee_task_count=Count('assigned_to__tasks')
    )

    if completed_tasks.count() < 10:
        print("Not enough historical data for training")
        return None

    # Prepare training data
    data = []
    for task in completed_tasks:
        # Text features
        title_length = len(task.title)
        desc_length = len(task.description or '')
        word_count = len((task.title + " " + (task.description or "")).split())
        
        # Priority and complexity
        priority_score = ['LOW', 'MEDIUM', 'HIGH', 'URGENT'].index(task.priority)
        
        # Project context
        project_complexity = task.project_task_count
        
        # Assignee experience (if available)
        assignee_experience = task.assignee_task_count if task.assigned_to else 0
        
        # Calculate complexity score based on keywords
        complexity_keywords = [
            'implement', 'integrate', 'refactor', 'database', 'auth', 'api',
            'migration', 'performance', 'security', 'architecture'
        ]
        complexity_score = sum(1 for keyword in complexity_keywords 
                             if keyword in (task.title + " " + (task.description or "")).lower())
        
        data.append({
            'title_length': title_length,
            'desc_length': desc_length,
            'word_count': word_count,
            'priority_score': priority_score,
            'project_complexity': project_complexity,
            'assignee_experience': assignee_experience,
            'complexity_score': complexity_score,
            'story_points': task.story_points
        })

    df = pd.DataFrame(data)
    X = df.drop('story_points', axis=1)
    y = df['story_points']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Story Points Model MSE: {mse:.2f}")
    
    # Save model
    model_dir = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(model, os.path.join(model_dir, 'story_points_model.pkl'))
    joblib.dump(X_train.columns.tolist(), os.path.join(model_dir, 'story_points_features.pkl'))
    
    return model


def train_sprint_risk_model():
    """
    Train a model to predict sprint completion risk.
    """
    completed_sprints = Sprint.objects.filter(status=Sprint.COMPLETED).annotate(
        total_points=Count('tasks'),
        completed_points=Count('tasks', filter=Q(tasks__status='DONE')),
        team_size=Count('tasks__assigned_to', distinct=True)
    )

    if completed_sprints.count() < 10:
        print("Not enough sprint data for training")
        return None

    data = []
    for sprint in completed_sprints:
        # Sprint features
        duration_days = (sprint.end_date - sprint.start_date).days
        total_points = sprint.total_points or 0
        completed_points = sprint.completed_points or 0
        completion_rate = completed_points / total_points if total_points > 0 else 0
        team_size = sprint.team_size
        
        # Risk label based on completion
        risk_level = 0 if completion_rate >= 0.9 else 1 if completion_rate >= 0.7 else 2  # LOW, MEDIUM, HIGH
        
        data.append({
            'duration_days': duration_days,
            'total_points': total_points,
            'team_size': team_size,
            'points_per_day': total_points / duration_days if duration_days > 0 else 0,
            'points_per_person': total_points / team_size if team_size > 0 else 0,
            'risk_level': risk_level
        })

    df = pd.DataFrame(data)
    X = df.drop('risk_level', axis=1)
    y = df['risk_level']

    # Split and train
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=8,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Sprint Risk Model Accuracy: {accuracy:.2f}")
    
    # Save model
    model_dir = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(model, os.path.join(model_dir, 'sprint_risk_model.pkl'))
    joblib.dump(X_train.columns.tolist(), os.path.join(model_dir, 'sprint_risk_features.pkl'))
    
    return model


def train_asset_recommender():
    """
    Train a TF-IDF based asset recommendation system.
    """
    # Collect asset data
    assets = Asset.objects.select_related('project').all()
    
    if assets.count() < 5:
        print("Not enough assets for training")
        return None

    # Prepare document corpus
    asset_documents = []
    asset_data = []
    
    for asset in assets:
        document = f"{asset.name} {asset.description} {asset.tags} {asset.asset_type}"
        asset_documents.append(document.lower())
        asset_data.append({
            'id': asset.id,
            'project_id': asset.project_id,
            'name': asset.name,
            'asset_type': asset.asset_type,
            'tags': asset.tags
        })
    
    # Train TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.8
    )
    
    tfidf_matrix = vectorizer.fit_transform(asset_documents)
    
    # Save model and data
    model_dir = os.path.dirname(os.path.abspath(__file__))
    joblib.dump(vectorizer, os.path.join(model_dir, 'asset_vectorizer.pkl'))
    joblib.dump(tfidf_matrix, os.path.join(model_dir, 'asset_tfidf_matrix.pkl'))
    joblib.dump(asset_data, os.path.join(model_dir, 'asset_data.pkl'))
    
    return vectorizer, tfidf_matrix, asset_data


def get_story_point_prediction(task_title, task_description, project_id=None):
    """
    Get ML-based story point prediction.
    """
    try:
        model_dir = os.path.dirname(os.path.abspath(__file__))
        model = joblib.load(os.path.join(model_dir, 'story_points_model.pkl'))
        feature_names = joblib.load(os.path.join(model_dir, 'story_points_features.pkl'))
        
        # Extract features
        title_length = len(task_title)
        desc_length = len(task_description or '')
        word_count = len((task_title + " " + (task_description or "")).split())
        
        priority_score = 2  # Default MEDIUM
        
        # Get project context
        from erp_projects.models import Project
        project_complexity = 10  # Default
        assignee_experience = 5   # Default
        
        if project_id:
            project_complexity = Project.objects.filter(id=project_id).annotate(
                task_count=Count('tasks')
            ).first().task_count or 10
        
        # Calculate complexity score
        complexity_keywords = [
            'implement', 'integrate', 'refactor', 'database', 'auth', 'api',
            'migration', 'performance', 'security', 'architecture'
        ]
        complexity_score = sum(1 for keyword in complexity_keywords 
                             if keyword in (task_title + " " + (task_description or "")).lower())
        
        # Create feature vector
        features = {
            'title_length': title_length,
            'desc_length': desc_length,
            'word_count': word_count,
            'priority_score': priority_score,
            'project_complexity': project_complexity,
            'assignee_experience': assignee_experience,
            'complexity_score': complexity_score
        }
        
        # Ensure all features are present in correct order
        feature_vector = [features.get(feature, 0) for feature in feature_names]
        
        # Predict
        prediction = model.predict([feature_vector])[0]
        return max(1, min(21, int(round(prediction))))  # Clamp to Fibonacci range
        
    except Exception as e:
        print(f"Story point prediction failed: {e}")
        return 3  # Fallback


def get_sprint_risk_prediction(sprint):
    """
    Get ML-based sprint risk prediction.
    """
    try:
        model_dir = os.path.dirname(os.path.abspath(__file__))
        model = joblib.load(os.path.join(model_dir, 'sprint_risk_model.pkl'))
        feature_names = joblib.load(os.path.join(model_dir, 'sprint_risk_features.pkl'))
        
        # Calculate sprint features
        duration_days = (sprint.end_date - sprint.start_date).days
        total_points = sprint.total_story_points()
        team_size = sprint.tasks.values('assigned_to').distinct().count()
        
        features = {
            'duration_days': duration_days,
            'total_points': total_points,
            'team_size': team_size,
            'points_per_day': total_points / duration_days if duration_days > 0 else 0,
            'points_per_person': total_points / team_size if team_size > 0 else 0
        }
        
        feature_vector = [features.get(feature, 0) for feature in feature_names]
        
        # Predict
        risk_prediction = model.predict([feature_vector])[0]
        risk_labels = ['LOW', 'MEDIUM', 'HIGH']
        
        return risk_labels[risk_prediction]
        
    except Exception as e:
        print(f"Sprint risk prediction failed: {e}")
        return "MEDIUM"  # Fallback


def get_asset_recommendations(project_id, task_title, limit=5):
    """
    Get ML-based asset recommendations for a task.
    """
    try:
        model_dir = os.path.dirname(os.path.abspath(__file__))
        vectorizer = joblib.load(os.path.join(model_dir, 'asset_vectorizer.pkl'))
        tfidf_matrix = joblib.load(os.path.join(model_dir, 'asset_tfidf_matrix.pkl'))
        asset_data = joblib.load(os.path.join(model_dir, 'asset_data.pkl'))
        
        # Filter assets by project
        task_query = f"{task_title}".lower()
        task_vector = vectorizer.transform([task_query])
        
        # Calculate similarities
        from sklearn.metrics.pairwise import cosine_similarity
        similarities = cosine_similarity(task_vector, tfidf_matrix).flatten()
        
        # Get top recommendations
        top_indices = similarities.argsort()[-limit:][::-1]
        
        recommendations = []
        for idx in top_indices:
            asset = asset_data[idx]
            if asset['project_id'] == project_id and similarities[idx] > 0.1:
                recommendations.append({
                    'type': 'ASSET',
                    'title': asset['name'],
                    'id': asset['id'],
                    'asset_type': asset['asset_type'],
                    'tags': asset['tags'],
                    'similarity_score': float(similarities[idx])
                })
        
        return recommendations[:limit]
        
    except Exception as e:
        print(f"Asset recommendation failed: {e}")
        return []  # Fallback


def train_all_models():
    """
    Train all ML models.
    """
    print("Training Story Points model...")
    train_story_point_model()
    
    print("Training Sprint Risk model...")
    train_sprint_risk_model()
    
    print("Training Asset Recommender...")
    train_asset_recommender()
    
    print("All models trained successfully!")