# Generated by Django 4.2.16 on 2024-11-19 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cur_unit', models.CharField(max_length=20)),
                ('cur_nm', models.CharField(max_length=20)),
                ('ttb', models.FloatField(null=True)),
                ('tts', models.FloatField(null=True)),
                ('deal_bas_r', models.FloatField()),
                ('bkpr', models.IntegerField(null=True)),
                ('yy_efee_r', models.FloatField(null=True)),
                ('ten_dd_efee_r', models.FloatField(null=True)),
                ('kftc_deal_bas_r', models.FloatField(null=True)),
                ('kftc_bkpr', models.IntegerField(null=True)),
                ('update_date', models.DateField()),
            ],
            options={
                'ordering': ['-update_date'],
                'indexes': [models.Index(fields=['cur_unit'], name='exchange_ex_cur_uni_5f15fa_idx'), models.Index(fields=['update_date'], name='exchange_ex_update__01bc55_idx')],
            },
        ),
        migrations.AddConstraint(
            model_name='exchangerate',
            constraint=models.UniqueConstraint(fields=('cur_unit', 'update_date'), name='unique_currency_date'),
        ),
    ]