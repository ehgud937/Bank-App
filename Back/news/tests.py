# news/tests.py
from django.test import TestCase
from .utils import NaverNewsCrawler

def test_crawler():
    crawler = NaverNewsCrawler()
    articles = crawler.get_finance_news()
    print("Found articles:", len(articles))
    if articles:
        print("First article:", articles[0])

