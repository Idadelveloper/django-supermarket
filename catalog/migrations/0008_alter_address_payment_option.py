# Generated by Django 3.2.4 on 2021-06-17 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='payment_option',
            field=models.CharField(choices=[('S', 'Stripe'), ('P', 'Paypal')], max_length=2),
        ),
    ]
