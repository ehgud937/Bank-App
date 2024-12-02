# recommendations/management/commands/generate_dummy_data.py
from django.core.management.base import BaseCommand
from recommend.ml_models import UserBasedRecommender

class Command(BaseCommand):
    help = 'Generate dummy data and train initial ML models'

    def handle(self, *args, **options):
        recommender = UserBasedRecommender()
        recommender._train_models()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully generated dummy data and trained models')
        )