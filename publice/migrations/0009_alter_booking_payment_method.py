# Generated by Django 5.0.6 on 2024-07-06 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publice', '0008_alter_booking_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='payment_method',
            field=models.CharField(choices=[('Cash on delivery', 'Cash on delivery'), ('Esewa', 'Esewa')], max_length=200, null=True),
        ),
    ]