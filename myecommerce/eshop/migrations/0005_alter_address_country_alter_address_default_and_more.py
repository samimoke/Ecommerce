# Generated by Django 4.2.4 on 2023-08-23 20:37

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0004_alter_address_address2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='default',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
