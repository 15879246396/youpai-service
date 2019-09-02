# Generated by Django 2.2.4 on 2019-09-01 15:56

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommodityTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(auto_now_add=True, verbose_name='gmt create')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='gmt modified')),
                ('delete_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未删除'), (1, '已删除')], default=0, verbose_name='删除状态')),
                ('title', models.CharField(max_length=64, verbose_name='分组标题')),
                ('prod_count', models.IntegerField(null=True, verbose_name='展示数量')),
                ('style', models.IntegerField(choices=[(1, '一列一个'), (2, '一列两个'), (3, '一列三个')], default=1, verbose_name='列表样式')),
                ('seq', models.IntegerField(default=0, verbose_name='排序')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('delete_status_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='IndexImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(auto_now_add=True, verbose_name='gmt create')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='gmt modified')),
                ('delete_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未删除'), (1, '已删除')], default=0, verbose_name='删除状态')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('img_url', models.URLField(verbose_name='图片')),
                ('des', models.CharField(blank=True, max_length=256, null=True, verbose_name='说明文字')),
                ('link', models.URLField(null=True, verbose_name='链接')),
                ('seq', models.IntegerField(default=0, verbose_name='排序')),
                ('type', models.IntegerField(choices=[(0, '商品')], default=0, verbose_name='关联类型')),
                ('relation', models.IntegerField(verbose_name='关联')),
            ],
            options={
                'ordering': ['-seq'],
            },
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(auto_now_add=True, verbose_name='gmt create')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='gmt modified')),
                ('delete_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未删除'), (1, '已删除')], default=0, verbose_name='删除状态')),
                ('title', models.CharField(max_length=64, verbose_name='公告标题')),
                ('content', models.TextField(verbose_name='公告内容')),
                ('is_top', models.BooleanField(default=False, verbose_name='是否置顶')),
                ('status', models.BooleanField(default=True, verbose_name='是否公布')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('delete_status_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
