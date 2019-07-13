#coding=utf-8

from django.shortcuts import render, redirect
from df_user.models import *
from df_goods.models import *
from django.http import JsonResponse, HttpResponseRedirect
from hashlib import sha1
from . import user_decorator

def register(request):
    context = {'page_name':1}
    return render(request,'df_user/register.html',context)

def register_exist(request):#ajax
    uname = request.GET['uname']
    count = UserInfo.objects.filter(uname = uname).count()
    return JsonResponse({'count':count})

def register_handle(request):
    #接收传输过来的数据
    uname = request.POST['user_name']
    upasswd = request.POST['pwd']
    upasswd2 = request.POST['cpwd']
    uemail = request.POST['email']
    if upasswd != upasswd2 or uname == '' or upasswd == '' or uemail == '':
        return redirect('/user/register/')
    else:
        #给密码加密
        s1 = sha1()
        s1.update(upasswd.encode('utf8'))
        upasswd3 = s1.hexdigest()
        #创建对象用于存储数据
        user = UserInfo()
        user.uname = uname
        user.upasswd = upasswd3
        user.uemail = uemail
        user.save()
        return redirect('/user/login/')

def login(request):
    uname = request.COOKIES.get('uname','')
    context = {'title':'用户登录', 'error_name':0, 'uname':uname,'page_name':1}
    return render(request, 'df_user/login.html', context)

def login_handle(request):
    #接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)
    #根据用户名查询对象
    user = UserInfo.objects.filter(uname = uname)#[]
    #判断：如果未查到用户名则为用户名错误，如果查到了则判断密码是否正确，正确则跳转到用户中心
    print(uname,upwd)
    if len(user) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))
        if s1.hexdigest() == user[0].upasswd:
            red = HttpResponseRedirect('/user/user_center_info/')
            #记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age = -1)
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录','page_name':1, 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd':upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录','page_name':1, 'error_name': 1,'error_pwd': 0, 'uname': uname, 'upwd':upwd}
        return render(request, 'df_user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

@user_decorator.login
def user_center_info(request):
    user_email = UserInfo.objects.get(id = request.session['user_id']).uemail
    #最近浏览
    goods_ids = request.COOKIES.get('goods_ids','')
    print(goods_ids)
    goods_ids1=goods_ids.split(',')
    print(goods_ids1)
    goods_list=[]
    for good_id in goods_ids1:
        try:
            goods_list.append(GoodsInfo.objects.get(id=int(good_id)))
        except ValueError:
            pass
    context = {
        'title': '用户中心','page_name':1,
        'user_name':request.session['user_name'],
        'user_email': user_email,
        'goods_list': goods_list,
    }
    return render(request, 'df_user/user_center_info.html', context)

@user_decorator.login
def user_center_order(request):
    context = {'title':'用户中心','page_name':1,}
    return render(request, 'df_user/user_center_order.html',context)

@user_decorator.login
def user_center_site(request):
    user = UserInfo.objects.get(id = request.session['user_id'])
    if request.method =='POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uZipcode = post.get('uZipcode')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title':'用户中心','page_name':1, 'user':user}
    return render(request, 'df_user/user_center_site.html', context)
