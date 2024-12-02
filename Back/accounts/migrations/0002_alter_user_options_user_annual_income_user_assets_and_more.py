# Generated by Django 4.2.16 on 2024-11-18 01:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '사용자', 'verbose_name_plural': '사용자 목록'},
        ),
        migrations.AddField(
            model_name='user',
            name='annual_income',
            field=models.BigIntegerField(default=0, help_text='단위: 원', validators=[django.core.validators.MinValueValidator(0)], verbose_name='연봉'),
        ),
        migrations.AddField(
            model_name='user',
            name='assets',
            field=models.BigIntegerField(default=0, help_text='단위: 원', validators=[django.core.validators.MinValueValidator(0)], verbose_name='보유자산'),
        ),
        migrations.AddField(
            model_name='user',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='생년월일'),
        ),
        migrations.AddField(
            model_name='user',
            name='investment_type',
            field=models.CharField(choices=[('CONSERVATIVE', '안정형'), ('MODERATE', '중립형'), ('AGGRESSIVE', '공격형'), ('SPECULATIVE', '위험추구형')], default='MODERATE', max_length=20, verbose_name='투자성향'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_social_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='primary_bank',
            field=models.CharField(choices=[('KB', 'KB국민은행'), ('SH', '신한은행'), ('WR', '우리은행'), ('NH', '농협은행'), ('IBK', '기업은행'), ('KEB', '하나은행'), ('ETC', '기타')], default='ETC', max_length=10, verbose_name='주거래은행'),
        ),
        migrations.AddField(
            model_name='user',
            name='social_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='social_provider',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
