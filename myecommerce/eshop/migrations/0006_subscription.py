# Generated by Django 4.1.4 on 2024-02-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0005_alter_address_country_alter_address_default_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
