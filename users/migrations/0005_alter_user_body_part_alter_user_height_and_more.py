# Generated by Django 5.0.2 on 2024-03-27 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_body_part_alter_user_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='body_part',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='height',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
