# Generated by Django 5.0.6 on 2024-07-07 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publice', '0010_alter_about_us_image_alter_about_us_introduction_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='payment_method',
            field=models.CharField(choices=[('Cash on delivery', 'Cash on delivery'), ('Esewa', 'Esewa')], max_length=200, null=True),
        ),
    ]
