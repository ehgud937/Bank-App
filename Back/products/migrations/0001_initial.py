# Generated by Django 4.2.16 on 2024-11-19 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepositProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField(unique=True)),
                ('kor_co_nm', models.TextField()),
                ('fin_prdt_nm', models.TextField()),
                ('etc_note', models.TextField()),
                ('join_deny', models.IntegerField()),
                ('join_member', models.TextField()),
                ('join_way', models.TextField()),
                ('spcl_cnd', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DepositOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fin_prdt_cd', models.TextField()),
                ('intr_rate_type_nm', models.CharField(max_length=100)),
                ('intr_rate', models.FloatField(default=-1)),
                ('intr_rate2', models.FloatField(default=-1)),
                ('save_trm', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.depositproducts')),
            ],
        ),
    ]
