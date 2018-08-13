# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class CartInfo(models.Model):
    user=models.ForeignKey('df_user.UserInfo',on_delete= models.CASCADE)
    goods=models.ForeignKey('df_goods.GoodsInfo',on_delete= models.CASCADE)
    count=models.IntegerField(default=0)