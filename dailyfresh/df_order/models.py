#coding=utf-8
from django.db import models

class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)
    user=models.ForeignKey('df_user.UserInfo',on_delete=models.CASCADE)
    odate=models.DateTimeField(auto_now=True)
    oIspay=models.BooleanField(default=False)
    ototal=models.DecimalField(max_digits=6, decimal_places=2)
    oaddress=models.CharField(max_length=150,default='')
#无法实现支付、物流信息

class OrderDetailInfo(models.Model):
    goods=models.ForeignKey('df_goods.GoodsInfo',on_delete=models.CASCADE)
    order=models.ForeignKey(OrderInfo,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    count=models.IntegerField()