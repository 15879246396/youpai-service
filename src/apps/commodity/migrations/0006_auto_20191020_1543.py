# Generated by Django 2.2.4 on 2019-10-20 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0005_auto_20191019_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freighttemplate',
            name='piece',
            field=models.IntegerField(null=True, verbose_name='需满件数'),
        ),
    ]
