# Generated by Django 2.1 on 2020-06-02 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20200602_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='authors',
            name='github_profile',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]