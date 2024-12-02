# Generated by Django 4.2.16 on 2024-11-21 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsKeyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=50, unique=True)),
                ('count', models.IntegerField(default=0)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-count'],
            },
        ),
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('url', models.URLField()),
                ('press', models.CharField(max_length=50)),
                ('published_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(max_length=50)),
                ('thumbnail_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-published_at'],
                'indexes': [models.Index(fields=['-published_at'], name='news_newsar_publish_db2481_idx'), models.Index(fields=['category'], name='news_newsar_categor_ed8dc2_idx')],
            },
        ),
    ]
