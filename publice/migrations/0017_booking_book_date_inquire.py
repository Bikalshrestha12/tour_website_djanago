# Generated by Django 5.0.6 on 2024-07-16 06:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publice', '0016_alter_booking_payment_method'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='book_date',
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name='Inquire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.IntegerField()),
                ('checking_date', models.DateField()),
                ('checkout_date', models.DateField()),
                ('destiantion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='publice.destination')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
