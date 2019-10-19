# Generated by Django 2.2.4 on 2019-09-01 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(auto_now_add=True, verbose_name='gmt create')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='gmt modified')),
                ('delete_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未删除'), (1, '已删除')], default=0, verbose_name='删除状态')),
                ('name', models.CharField(max_length=64, verbose_name='产品类目名称')),
                ('pic', models.URLField(null=True, verbose_name='类目的显示图片')),
                ('seq', models.IntegerField(verbose_name='排序')),
            ],
            options={
                'ordering': ['-seq'],
            },
        ),
        migrations.CreateModel(
            name='FreightTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(auto_now_add=True, verbose_name='gmt create')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='gmt modified')),
                ('delete_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未删除'), (1, '已删除')], default=0, verbose_name='删除状态')),
                ('name', models.CharField(max_length=64, verbose_name='模板名称')),
                ('freight', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='运费')),
                ('charge_type', models.IntegerField(choices=[(0, '满件数'), (1, '满金额'), (2, '满件数或者满金额')], verbose_name='收费方式')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='需满金额')),
                ('piece', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='需满件数')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(auto_now_add=True, verbose_name='gmt create')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='gmt modified')),
                ('delete_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未删除'), (1, '已删除')], default=0, verbose_name='删除状态')),
                ('name', models.CharField(max_length=64, verbose_name='产品名称')),
                ('ori_price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='原价')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='现价')),
                ('is_free_fee', models.BooleanField(default=True, verbose_name='是否包邮')),
                ('brief', models.CharField(blank=True, max_length=512, null=True, verbose_name='简要描述')),
                ('content', models.TextField(null=True, verbose_name='详细描述')),
                ('pic', models.URLField(null=True, verbose_name='产品主图')),
                ('images', models.CharField(blank=True, max_length=1024, null=True, verbose_name='产品图片')),
                ('sold_num', models.IntegerField(default=0, null=True, verbose_name='销量')),
                ('total_stocks', models.IntegerField(default=0, verbose_name='总库存')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='commodity.Category')),
                ('commodity_tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='index.CommodityTag')),
                ('freight_template', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='commodity.FreightTemplate', verbose_name='运费模板')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]