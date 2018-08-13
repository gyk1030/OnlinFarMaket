# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.test import TestCase
from django.shortcuts import render, HttpResponse
from df_goods.models import GoodsInfo, TypeInfo
# Create your tests here.

import random
def cut(q, w, e, r):
    with open('static/images/RandomWord.txt','r',encoding='utf-8')as f:
        a = 10
        b = 60
        while True:
            a = random.randint(q, w)
            b = random.randint(q, w)
            if a > b:
                c = a
                a = b
                b = c
            if b - a > e and b - a < r:
                break
        data = f.read()
        c = data[a:b]
    return c

def test2():
    dict = ['水果', '水产', '肉类', '蛋类', '蔬菜', '速冻']
    for i in dict:
        TypeInfo.objects.create(ttitle=i)
    print('************ TypeInfo is ok *************')

def test1(folder,s,id):
    list = []
    for i in range(s):
        c = cut(10, 1000, 30, 80)
        d = cut(10, 1000, 5, 15)
        gtitle = '柠檬'
        i = str(i+1).zfill(2)
        gpic = 'images/%s/image0%s.jpg'%(folder,i)
        gprice = random.randint(5, 30)
        gunit = '500g'
        gclick = random.randint(10,500)
        gjianjie = d
        gkucun = random.randint(0,1000)
        gcontent = c
        gtype_id = id
        dict = {'gtitle':gtitle,'gpic':gpic,'gprice':gprice,'gunit':gunit,'gclick':gclick,
                'gjianjie':gjianjie,'gkucun':gkucun,'gcontent':gcontent,'gtype_id':gtype_id}
        list.append(dict)
    for i in list:
        GoodsInfo.objects.create(**i)
    print('************ GoodsInfo is ok *************')


def test(request):
    test2()
    test1('fruits', 30, 1)
    test1('seafoods', 21, 2)
    test1('meets', 19, 3)
    test1('vegetables', 18,5)
    test1('eggs', 16, 4)
    test1('freeze', 17, 6)
    return HttpResponse('ok')

