#coding=utf-8

from django.shortcuts import render
from df_goods.models import *
from django.core.paginator import Paginator,Page
from django.views.decorators.cache import cache_page


#缓存
@cache_page(60 * 15)
def index(request):
    # #查询各分类的最新4条数据、最热4条数据
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'title': '首页', 'guest_cart': 1,
               'type0': type0, 'type01': type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51,
               }
    typeinfo = TypeInfo.objects.get(pk=4)
    print(typeinfo)
    return render(request, 'df_goods/index.html', context)

#缓存
@cache_page(60 * 15)
def list(request, tid, pingdex, sort):
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':#按照默认最新排序
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
        #此方法同样可行，通过TypeInfo的ID查询对应的商品信息
        # goods_list = typeinfo.goodsinfo_set.order_by('-id')
    elif sort == '2':#按照价格排序
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':#按照点击量排序
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator = Paginator(goods_list, 10)
    page=paginator.page(int(pingdex))
    context={'title':typeinfo.ttitle,
             'guest_cart':1,
             'page':page,
             'paginator':paginator,
             # 'typeinfo': typeinfo,
             'sort':sort,
             'news':news,
             'tid':tid}
    # goods = GoodsInfo.objects.get(pk=int(id))
    return render(request, 'df_goods/list.html', context)

def detail(request, id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick = goods.gclick+1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'title':goods.gtype.ttitle,
               'guest_cart':1,
               'g':goods,
               'news':news,
               'id':id
               }
    response=render(request, 'df_goods/detail.html', context)
    # return render(request, 'df_goods/detail.html')
    #记录最近浏览，在用户中心使用
    goods_ids=request.COOKIES.get('goods_ids','')
    goods_id='%d'%goods.id
    if goods_ids!='':#判断是否有浏览记录，如果有则继续判断
        goods_ids1=goods_ids.split(',')#拆分为列表
        if goods_ids1.count(goods_id)>=1:#如果商品已经被记录，则删除
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)#添加到第一个
        if len(goods_ids1)>=6:#如果超过6个则删除最后一个
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids=goods_id#如果没有浏览记录则直接加
    response.set_cookie('goods_ids',goods_ids)#写入cookie
    return response