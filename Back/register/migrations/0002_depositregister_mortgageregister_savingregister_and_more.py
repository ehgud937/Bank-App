# Generated by Django 4.2.16 on 2024-11-22 01:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_mortgageproducts_mortgageotions'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', '신청중'), ('ACTIVE', '가입완료'), ('EXPIRED', '만기'), ('CANCELLED', '해지')], default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registers', to='products.depositoptions')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registers', to='products.depositproducts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposit_registers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MortgageRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', '신청중'), ('ACTIVE', '가입완료'), ('EXPIRED', '만기'), ('CANCELLED', '해지')], default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registers', to='products.mortgageotions')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registers', to='products.mortgageproducts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mortgage_registers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SavingRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', '신청중'), ('ACTIVE', '가입완료'), ('EXPIRED', '만기'), ('CANCELLED', '해지')], default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registers', to='products.savingoptions')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registers', to='products.savingproducts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saving_registers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Register',
        ),
    ]
