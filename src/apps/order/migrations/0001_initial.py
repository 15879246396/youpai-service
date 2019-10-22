# Generated by Django 2.2.4 on 2019-10-22 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import order.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mine', '0003_area_shippingaddr'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('commodity', '0006_auto_20191020_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(auto_now_add=True, verbose_name='gmt create')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='gmt modified')),
                ('name', models.CharField(max_length=32, verbose_name='名称')),
                ('home_url', models.URLField(verbose_name='官网')),
                ('query_url', models.URLField(verbose_name='查件地址')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(auto_now_add=True, verbose_name='gmt create')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='gmt modified')),
                ('delete_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未删除'), (1, '已删除')], default=0, verbose_name='删除状态')),
                ('order_sn', models.CharField(default=order.utils.generate_ordering_no, max_length=128, verbose_name='订单号')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='订单价格')),
                ('reduce_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='优惠金额')),
                ('status', models.IntegerField(choices=[(1, '待付款'), (2, '待发货'), (3, '待收货'), (4, '待评价'), (5, '成功'), (6, '失败')], default=1, verbose_name='订单状态')),
                ('product_nums', models.IntegerField(verbose_name='订单商品总数')),
                ('pay_status', models.BooleanField(default=False, verbose_name='支付状态')),
                ('pay_type', models.IntegerField(choices=[(1, '微信支付'), (2, '支付宝支付'), (3, '手动代付')], default=1, verbose_name='支付方式')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='订单支付(完成)时间')),
                ('freight_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=15, verbose_name='订单运费')),
                ('shipment_no', models.CharField(max_length=128, null=True, verbose_name='物流单号')),
                ('dvy_time', models.DateTimeField(blank=True, null=True, verbose_name='发货时间')),
                ('finally_time', models.DateTimeField(blank=True, null=True, verbose_name='订单完成时间')),
                ('cancel_time', models.DateTimeField(blank=True, null=True, verbose_name='订单取消时间')),
                ('close_type', models.IntegerField(choices=[(1, '超时未支付'), (2, '退款关闭'), (3, '买家取消'), (4, '买家取消'), (5, '已通过货到付款交易')], default=1, verbose_name='订单关闭原因')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Delivery')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order', to=settings.AUTH_USER_MODEL)),
                ('user_addr', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order', to='mine.ShippingAddr', verbose_name='用户订单地址')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gmt_create', models.DateTimeField(auto_now_add=True, verbose_name='gmt create')),
                ('gmt_modified', models.DateTimeField(auto_now=True, verbose_name='gmt modified')),
                ('delete_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未删除'), (1, '已删除')], default=0, verbose_name='删除状态')),
                ('count', models.IntegerField(verbose_name='商品数量')),
                ('comment_status', models.BooleanField(default=False, verbose_name='是否评价')),
                ('commodity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.Commodity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order', to='order.Order')),
                ('specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commodity.Specification')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderRefund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_status', models.PositiveSmallIntegerField(blank=True, choices=[(0, '未删除'), (1, '已删除')], default=0, verbose_name='删除状态')),
                ('refund_sn', models.CharField(default=order.utils.generate_ordering_no, max_length=128, verbose_name='退款编号')),
                ('apply_time', models.DateTimeField(auto_now_add=True, verbose_name='申请时间')),
                ('buyer_msg', models.CharField(max_length=128, verbose_name='退款原因')),
                ('photo_files', models.CharField(default='[]', max_length=64, verbose_name='凭证文件id列表')),
                ('apply_type', models.IntegerField(choices=[(1, '仅退款'), (2, '退款退货')], default=1, verbose_name='申请类型')),
                ('refund_status', models.IntegerField(choices=[(1, '待审核'), (2, '同意'), (3, '不同意')], default=1, verbose_name='处理状态')),
                ('return_status', models.IntegerField(choices=[(0, '退款处理中'), (1, '退款成功'), (-1, '退款失败')], default=0, verbose_name='退款状态')),
                ('pay_type', models.IntegerField(choices=[(1, '微信支付'), (2, '支付宝'), (3, '其他')], null=True, verbose_name='退款方式')),
                ('out_refund_no', models.CharField(max_length=128, verbose_name='第三方退款单号(微信退款单号)')),
                ('pay_type_name', models.CharField(max_length=64, verbose_name='订单支付名称')),
                ('refund_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='退款金额')),
                ('handel_time', models.DateTimeField(null=True, verbose_name='卖家处理时间')),
                ('refund_time', models.DateTimeField(null=True, verbose_name='退款时间')),
                ('seller_msg', models.CharField(max_length=128, verbose_name='卖家备注')),
                ('delivery_no', models.CharField(max_length=128, null=True, verbose_name='物流单号')),
                ('ship_time', models.DateTimeField(null=True, verbose_name='发货时间')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Delivery')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.Order')),
                ('order_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refund', to='order.OrderItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='refund', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
