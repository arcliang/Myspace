from django.shortcuts import render,render_to_response
from .models import *
import time
# Create your views here.
from django.http import HttpResponseRedirect
def showregister(request):
    return render(request,'myblog/register.html')

def register(request):    #注册函数
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        UserResult = User.objects.filter(username=username)  #判断是否已有此用户
        if (len(UserResult)>0):
            FailRegisterResult = '用户已存在！'
            return render(request,'myblog/register.html',{'failregisterresult':FailRegisterResult})
        else:
            userResult = User.objects.create(username=username,password=password)
            userResult.save()
            SuccessLoginResult = '注册成功！请登录'
            return render(request,'myblog/login.html',{'successloginresult':SuccessLoginResult})

    else:
        pass
def showlogin(request):
    return render(request,'myblog/login.html')

def login(request):  #登录函数
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        RegisterResult = User.objects.filter(username=username,password=password)
        if (len(RegisterResult)>0):
            request.session['name'] = username
            return HttpResponseRedirect('/index')
        else:
            FailLoginResult = '该用户不存在或密码错误！'
            return render(request,'myblog/login.html',{'failloginresult':FailLoginResult})
    else:
        pass

def index(request):
    category = Category.objects.all()
    username = request.session.get('name')
    return render(request,'myblog/index.html',{'category':category,
                                               'username':username})

def category(request,id):
    category = Category.objects.get(pk=id)
    article = Article.objects.filter(category_id=id)
    print('文章内容：',article)
    username = request.session.get('name')
    return render(request,'myblog/article.html',{'article':article,
                                                 'category':category,
                                                 'username':username})

def articledetail(request,article_id):
    article_detail = Article.objects.get(id = article_id)
    article_category = Category.objects.get(pk = article_detail.category_id)
    username = request.session.get('name')
    return render(request,'myblog/articledetail.html',{'article_detail':article_detail,'article_category':article_category,
                                                       'username':username})

def logout(request):
    request.session.clear()
    return HttpResponseRedirect('/index')

def showuseredit(request):
    category = Category.objects.all()
    tags = Tag.objects.all()
    return render(request,'myblog/useredit.html',{'category':category,
                                                  'tags':tags})

def useredit(request):
    title = request.POST.get('title')
    body = request.POST.get('body')
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print('时间：',date)
    category = request.POST.get('category')
    tags = request.POST.get('tags')
    editer = request.session.get('name')
    if editer == None:
        editerisnull = '你还未登录，请登录后再创作！'
        return render(request,'myblog/login.html',{'editerisnull':editerisnull})
    else:
        category_id = Category.objects.get(name=category)
        tags_id = Tag.objects.get(name=tags)
        editer_id = User.objects.get(username=editer)
        Article_Update = Article.objects.create(title=title,body=body,date=date,category_id=category_id.id,tags_id=tags_id.id,editer_id=editer_id.id)
        Article_Update.save()

        return HttpResponseRedirect('/category/{}'.format(category_id.id))
