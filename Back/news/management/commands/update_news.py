# news/management/commands/update_news.py
from django.core.management.base import BaseCommand
from news.utils import NaverNewsCrawler

class Command(BaseCommand):
    help = 'Update news articles from Naver'

    def handle(self, *args, **kwargs):
        crawler = NaverNewsCrawler()
        crawler.update_news()
        self.stdout.write(self.style.SUCCESS('Successfully updated news'))