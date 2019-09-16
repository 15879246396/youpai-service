# Generated by Django 2.2.5 on 2019-09-16 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='产品规格名称')),
                ('commodity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commodity_specification', to='commodity.Commodity')),
            ],
        ),
    ]
