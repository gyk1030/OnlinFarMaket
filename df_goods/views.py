# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from df_goods.models import GoodsInfo, TypeInfo
from df_cart.models import CartInfo
from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
# 查询每类商品最新的4个和点击率最高的4个
def index(request):
    """
    index函数负责查询页面中需要展示的商品内容，
    主要是每类最新的4种商品和4中点击率最高的商品，
    每类商品需要查询2次
    """
    count = request.session.get('count')
    fruit = GoodsInfo.objects.filter(gtype__id=1).order_by("-gclick")[0:4]
    fish = GoodsInfo.objects.filter(gtype__id=2).order_by("-gclick")[:4]
    meat = GoodsInfo.objects.filter(gtype__id=3).order_by("-gclick")[:4]
    egg = GoodsInfo.objects.filter(gtype__id=4).order_by("-gclick")[:4]
    vegetables = GoodsInfo.objects.filter(gtype__id=5).order_by("-gclick")[:4]
    frozen = GoodsInfo.objects.filter(gtype__id=6).order_by("-gclick")[:4]
    # count = CartInfo.objects.filter(
    #     user_id=request.session.get('userid')).count()   'count':count,
    # # 构造上下文
    context = {'title': '首页', 'fruit': fruit,
               'fish': fish, 'meat': meat, 'egg': egg,
               'vegetables': vegetables, 'frozen': frozen,
               'guest_cart': 1,'page_name':0,'count':count}
    # print('*********************',fruit[0].gpic)
    # 返回渲染模板
    return render(request, 'df_goods/index.html', context)


#商品列表
def goodlist(request, typeid, pageid, sort):
    empty = []
    """
    goodlist函数负责展示某类商品的信息。
    url中的参数依次代表
    typeid:商品类型id;selectid:查询条件id，1为根据id查询，2位根据价格查询，3位根据点击量查询
    """
    count = request.session.get('count')
    # 获取最新发布的商品
    newgood = GoodsInfo.objects.all().order_by('-id')[:2]
    # 根据条件查询所有商品
    sumGoodList = []
    if sort == '1':#按最新   gtype_id  , gtype__id  指typeinfo_id
        sumGoodList = GoodsInfo.objects.filter(
            gtype_id=typeid).order_by('-id')
    elif sort == '2':#按价格
        sumGoodList = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('gprice')
    elif sort == '3':#按点击量
        sumGoodList = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('-gclick')
    # 分页
    paginator = Paginator(sumGoodList, 10)
    goodList = paginator.page(int(pageid))
    pindexlist = paginator.page_range
    # print pindexlist    xrange(1,2)
    # 确定商品的类型
    goodtype = ''
    try:
        goodtype = TypeInfo.objects.get(id=typeid)
    except:pass
    #
    # count = CartInfo.objects.filter(
    #     user_id=request.session.get('userid')).count()
    # 构造上下文  'count': count,
    context = {'title': '商品详情',  'list': 1,
               'guest_cart': 1, 'goodtype': goodtype,
               'newgood': newgood, 'goodList': goodList,
               'typeid': typeid, 'sort': sort,'empty':empty,
               'pindexlist': pindexlist, 'pageid': int(pageid),'count':count}

    # 渲染返回结果
    return render(request, 'df_goods/list.html', context)


def detail(request,id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick=goods.gclick+1
    goods.save()
    # 查询当前商品的类型
    goodtype = goods.gtype

    count = request.session.get('count')
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]

    context={'title':goods.gtype.ttitle,
             'guest_cart':1,
             'g':goods,
             'newgood':news,
             'id':id,
             'isDetail': True,
             'list':1,
             'goodtype': goodtype,
             'count':count}
    response=render(request,'df_goods/detail.html',context)


    #使用cookies记录最近浏览的商品id

    #获取cookies
    goods_ids = request.COOKIES.get('goods_ids', '')
    #获取当前点击商品id
    goods_id='%d'%goods.id
    #判断cookies中商品id是否为空
    if goods_ids!='':
        #分割出每个商品id
        goods_id_list=goods_ids.split(',')
        #判断商品是否已经存在于列表
        if goods_id_list.count(goods_id)>=1:
            #存在则移除
            goods_id_list.remove(goods_id)
        #在第一位添加
        goods_id_list.insert(0,goods_id)
        #判断列表数是否超过5个
        if len(goods_id_list)>=6:
            #超过五个则删除第6个
            del goods_id_list[5]
        #添加商品id到cookies
        goods_ids=','.join(goods_id_list)
    else:
        #第一次添加，直接追加
        goods_ids=goods_id
    response.set_cookie('goods_ids',goods_ids)

    print('321321321321321321321')
    return response

def search(request,pageid,sort):
    if request.method == 'POST':
        keywords = request.POST.get('keywords')
        sumGoodList = GoodsInfo.objects.filter(Q(gpic__icontains=keywords) | Q(gjianjie__icontains=keywords)).order_by('-id')
        newgood = GoodsInfo.objects.all().order_by('-id')[:2]
        # 将关键字加入session，用于下次查询
        request.session['keywords'] = keywords
        # 分页
        paginator = Paginator(sumGoodList, 22)
        goodList = paginator.page(int(pageid))
        pindexlist = paginator.page_range
        context = {
            'goodList':goodList,
            'pindexlist':pindexlist,
            'newgood':newgood,
            'guest_cart': 1,
            'pageid':int(pageid),
            'sort':sort
        }
        # print('*-*-*-*:',pindexlist,'---',pageid)
        return render(request, 'df_goods/search.html', context)
    else:
        context = search_help(request,pageid, sort)
        return render(request, 'df_goods/search.html', context)

def search_help(request,pageid,sort):
    keywords = request.session.get('keywords')
    sumGoodList = GoodsInfo.objects.filter(Q(gpic__icontains=keywords) | Q(gjianjie__icontains=keywords)).order_by('-id')
    newgood = GoodsInfo.objects.all().order_by('-id')[:2]
    # 判断排序类型
    sgl = sumGoodList
    if int(sort) == 1:
        sgl = sumGoodList
    elif int(sort) == 2:
        sgl = sumGoodList.order_by('gprice')
    elif int(sort) == 3:
        sgl = sumGoodList.order_by('-gclick')
    paginator = Paginator(sgl, 22)
    goodList = paginator.page(int(pageid))
    pindexlist = paginator.page_range
    context = {
        'goodList': goodList,
        'pindexlist': pindexlist,
        'newgood': newgood,
        'guest_cart': 1,
        'pageid': int(pageid),
        'sort':sort
    }
    return context