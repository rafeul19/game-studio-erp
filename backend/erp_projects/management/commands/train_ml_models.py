from django.core.management.base import BaseCommand
from erp_projects.ml.train_models import train_all_models


class Command(BaseCommand):
    help = 'Train machine learning models for AI predictions'

    def handle(self, *args, **options):
        self.stdout.write('Starting ML model training...')
        train_all_models()
        self.stdout.write(self.style.SUCCESS('ML models trained successfully!'))