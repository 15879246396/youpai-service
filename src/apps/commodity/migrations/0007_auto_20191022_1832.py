# Generated by Django 2.2.4 on 2019-10-22 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0006_auto_20191020_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(auto_now_add=True, verbose_name='gmt create')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='gmt modified')),
                ('delete_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未删除'), (1, '已删除')], default=0, verbose_name='删除状态')),
                ('type', models.IntegerField(choices=[(1, '全场通用'), (2, '指定商品可用')], default=1, verbose_name='优惠类型')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=15, verbose_name='优惠金额')),
                ('condition', models.DecimalField(decimal_places=0, max_digits=15, verbose_name='需满金额')),
                ('min_data', models.DateTimeField(verbose_name='有效期（后）')),
                ('max_data', models.DateTimeField(verbose_name='有效期（前）')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='freighttemplate',
            name='area_list',
            field=models.CharField(max_length=128, null=True, verbose_name='包邮省id列表'),
        ),
        migrations.AlterField(
            model_name='freighttemplate',
            name='charge_type',
            field=models.IntegerField(choices=[(0, '满件数'), (1, '满金额'), (2, '满件数或者满金额'), (3, '指定地区包邮')], verbose_name='收费方式'),
        ),
        migrations.AddField(
            model_name='commodity',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commodity', to='commodity.Coupon', verbose_name='优惠券'),
        ),
    ]
