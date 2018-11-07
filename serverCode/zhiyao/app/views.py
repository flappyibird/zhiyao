from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from app import models
import time
# Create your views here.

#实现用户登陆功能
def login(request):
    if request.method=='POST':
        userphone=request.POST.get('username')
        password=request.POST.get('password')
        if userphone and password:
            userphone=userphone.strip()
            try:
                user=models.User.objects.get(userphonenum=userphone)
                if user.password==password:
                    request.session['is_login']=True
                    request.session['userphone']=user.userphonenum
                    request.session['username']=user.username
                    #get是获取单个对象，filte是设置筛选条件
                    incubators=models.Incubator.objects.filter(user_userid=userphone)
                    incuName=[]
                    incuID=[]
                    incu=[]
                    for item in incubators:
                        incuName.append(item.incuname)
                        incuID.append(item.incuno)
                        incu=zip(incuName,incuID)
                    return render(request,'incubator.html',{"incu":incu})
                    #return render(request,"incubator.html",{"a":1})
                    #return redirect('/incubator/')
                else:
                    message='密码错误'
                    return render(request,'login.html',{'message':message})
            except:
                message='用户不存在'
                return render(request,'login.html',{'message':message})
    return render(request,'login.html')

#用户注册
def register(request):
    if request.method=='POST':
        userphone=request.POST.get('userphone')
        password=request.POST.get('password')
        usermail=request.POST.get('usermail')
        username=request.POST.get("username")
        try:
            user=models.User.objects.get(userphonenum=userphone)
            message = '此用户已存在'
            return render(request, 'register.html', {'message': message})
        except:
            try:
                user=models.User.objects.get(usermail=usermail)
                message = '此邮箱已被注册'
                return render(request, 'register.html', {'message': message})
            except:
                try:
                    user=models.User.objects.get(username=username)
                    message = '此用户名已被注册'
                    return render(request, 'register.html', {'message': message})
                except:
                    #userid和userphone是一样的
                    newUser = models.User()
                    newUser.userid = userphone
                    newUser.userphonenum = userphone
                    newUser.username = username
                    newUser.usermail = usermail
                    newUser.password=password
                    newUser.save()
                    return redirect('/login/')
    return render(request,'register.html')


#通过用户id也就是手机号获取用户所有正在使用的培养箱
def getIncubator(userid):
    incubators=models.Incubator.objects.get(user_userid=userid)
    return incubators
    #获取用户所有正在使用的培养箱

def incubator(request):
    pass
    return render(request,'incubator.html')

#查看培养箱的详细信息
def incubatorDeatil(request,incubatorno):
    #这个incubatorno传递进来的是培养箱的编号
    #需要再调用方法找到现在正在使用的培养箱的编号
    #此处需要从培养箱的首页传递要查看培养箱的id
    #此处假设获得，使用数据库中的 incubatorusing的id为i0101
    #iuno='i0101'
    print("pie"+incubatorno)
    ino=incubatorno
    initalInfo=getInital(ino)
    monitorInfo=getCurrent(ino)
    iuno=getIncubatorusingID(ino)

    #将当前用户访问的培养箱的信息存放再session重
    request.session['incubatorid']=iuno
    #session中的inid用于之后的页面重定向
    request.session['inid']=ino
    request.session['true']=True
    #将包含初始信息和当前监控信息的两个字典合并起来
    info={}
    info.update(initalInfo)
    info.update(monitorInfo)
    # info=combineDict(initalInfo,monitorInfo)
    print(info)
    return render(request,"incubatorDetail.html",info)

#辅助的功能函数 将两个字典合并
def combineDict(dic1,dic2):
    info={}
    return combineDict(dic1,dic2)


#通过培养箱的id获得当前正在使用的这个incubatorusing的id
def getIncubatorusingID(iuno):
    inusing=models.Incubatorusing.objects.filter(incubator_incuno=iuno).last()
    #这里需要注意的是，django里的外键是对象，不只是id
    return inusing.iuno

# 获取培养箱的初始信息，并在页面种显示出来
def getInital(ino):
    iuno=getIncubatorusingID(ino)
    #传入的是培养箱的id
    #这里需要使用的是incubatorusing的id
    try:
        #获取培养箱的初始信息
        incubatorUsing=models.Incubatorusing.objects.get(iuno=iuno)
        #print(incubatorUsing.itemperature)
        #很气人啊，在model里面，所有的id都会变成小写
        item=incubatorUsing.itemperature
        ihum=incubatorUsing.ihumidity
        ipre=incubatorUsing.ipressure
        ilig=incubatorUsing.ilightlntensity
        info={"Itemperature":item,"Ihumidity":ihum,"Ipressure":ipre,"IlightIntensity":ilig,"IisSucceed":True}
        return info
    except:
        info={"IisSucceed":True}
        return info

#获得培养箱内的最新监控信息
def getCurrent(ino):
    iuno=getIncubatorusingID(ino)
    try:
        monitorInfo=models.Monitorinform.objects.filter(incubatorusing_iuno=iuno).order_by("mtime").last()
        mtem=monitorInfo.mtemperature
        mhum=monitorInfo.mhumidity
        mpre=monitorInfo.mpressure
        mlig=monitorInfo.mlightlntensity
        info = {"Mtemperature": mtem, "Mhumidity": mhum, "Mpressure": mpre, "MlightIntensity": mlig, "MisSucceed": True}
        return info
    except:
        info={"MisSucceed":True}
        return info


#由正在使用的培养箱的id获得培养箱本身的id
def getIncubatorID(iuno):
    try:
        Incubatorusing=models.Incubatorusing.objects.get(iuno=iuno)
        inno=Incubatorusing.incubator_incuno
        return inno
    except:
        print("寻找培养箱时发生错误")
    return 0

#修改培养箱的环境信息
def alterenviroment(request,incubatorno):
    print("jingruhanshu")
    if request.method=="POST":
        AlightIntensity=request.POST.get('AlightIntensity')
        Atemperature=request.POST.get("Atemperature")
        Ahumidity=request.POST.get("Ahumidity")
        Apressure=request.POST.get("Apressure")
        incubatorusing_iuno=incubatorno
        #修改信息的id使用正在使用的培养箱的编号加上提交修改的时间戳
        alteid=incubatorusing_iuno+str(time.time())
        print("xiugaile"+alteid)

        newAlter=models.Alterenvironment()
        newAlter.alteid=alteid
        newAlter.alightlntensity=AlightIntensity
        newAlter.atemperature=Atemperature
        newAlter.ahumidity=Ahumidity
        newAlter.apressure=Apressure
        #将植物所处的阶段默认设置为0
        newAlter.aplantstage='0'
        newAlter.save()
        inno=str(getIncubatorID(incubatorno).incuno)
        print(inno)
        urlr="/incubatorDetail/"+inno+"/"
    return redirect(urlr)

def bbs(request):
    return render(request,'bbs.html')

def my(request):
    return render(request,'my.html')

def writePurchase(request):
    return render(request,'writePurchase.html')

def writeSelling(request):
    return render(request,"writeSelling.html")

def writeCommunication(request):
    return render(request,"wirteCommunication.html")

def savePurchase(request,userphone):
    if request.method=='POST':
        pid=str(userphone)+str(time.time())
        pMedicine=request.POST.get('pMedicine')
        pPrice=request.POST.get("pPrice")
        pDescribe=request.POST.get("pDescribe")
        pPhone=request.POST.get("pPhone")

        newBuy=models.Buypost()
        newBuy.bid=pid
        newBuy.bplant=pMedicine
        newBuy.bprice=pPrice
        newBuy.bdescription=pDescribe
        newBuy.bphonenum=pPhone
        usr=models.User.objects.get(userid=userphone)
        newBuy.user_userid=usr
        newBuy.save()
    return redirect("/bbs/")

def saveSelling(request,userphone):
    return redirect('/bbs/')

def saveCommunication(request,userphone):
    return redirect('/bbs/')

def getPurchase(request):
    print("尝试成功")
    #return HttpResponse('执行成功')
    return render(request,'bbs.html')

def getSelling(request):
    return HttpResponse("selling")

def getAll(request):
    return HttpResponse('all')

def getMy():
    pass

def getbbs(request):
    #把所有的信息都展示出来
    clist=models.Commentpost.objects.all().order_by('-releasectime')
    slist=models.Sellpost.objects.all().order_by('-releasestime')
    plist=models.Buypost.objects.all().order_by('-releasebtime')
    return render(request,'bbs.html',{'clist':clist,'slist':slist,'plist':plist})

#购买
def getPDetail(request,id):
    try:
        purchase=models.Buypost.objects.get(bid=id)
        return render(request,'purchaseDetail.html',{"pDetail":purchase,'success':True})
    except:
        return render(request,'bbs.html',{'success':False})

def getSDetail(request,id):
    try:
        selling=models.Sellpost.objects.get(sid=id)
        return render(request,'sellingDetail.html',{'sDetail':selling,'success':True})
    except:
        return render(request,'bbs.html',{'success':False})

def getCDetail(request,id):
    try:
        communication=models.Commentpost.objects.get(cid=id)
        return render(request,'communicationDetail.html',{'cDetail':communication,'success':True})
    except:
        print('meizhaodao')
        return render(request,'bbs.html',{'success':False})
