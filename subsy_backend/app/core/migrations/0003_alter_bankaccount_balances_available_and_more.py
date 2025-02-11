# Generated by Django 5.1.3 on 2025-02-07 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_bankaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='balances_available',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='balances_current',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='balances_iso_currency_code',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='balances_limit',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='official_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='subtype',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='type',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
