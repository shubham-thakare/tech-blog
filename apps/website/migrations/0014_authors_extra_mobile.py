# Generated by Django 2.1 on 2020-06-03 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_authors_mobile'),
    ]

    operations = [
        migrations.AddField(
            model_name='authors',
            name='extra_mobile',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
