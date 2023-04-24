# Generated by Django 3.2.16 on 2023-04-24 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20230424_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='posts.group', verbose_name='Группа поста'),
        ),
    ]