# Generated by Django 3.2.4 on 2021-06-16 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210616_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(default='NEW', max_length=200),
            preserve_default=False,
        ),
    ]
