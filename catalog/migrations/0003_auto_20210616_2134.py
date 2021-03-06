# Generated by Django 3.2.4 on 2021-06-16 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Shirt'), ('SW', 'SportWear'), ('OW', 'OutWear')], default='S', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.TextField(default='test description'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('S', 'secondary'), ('P', 'Primary'), ('D', 'Danger')], default=1, max_length=2),
            preserve_default=False,
        ),
    ]
