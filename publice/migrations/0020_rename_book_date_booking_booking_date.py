# Generated by Django 5.0.6 on 2024-07-23 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publice', '0019_alter_booking_payment_method'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='book_date',
            new_name='booking_date',
        ),
    ]