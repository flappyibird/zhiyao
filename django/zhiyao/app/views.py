from django.shortcuts import render
from app.models import User
from app.models import ChangeLog
from app.models import ViewParam
from django.views.decorators import csrf
from django.http import HttpResponse
import re,time,socket,os
# Create your views here.

#一条变更记录的顺序是温度、压强、湿度、光照
#处理来自硬件的请求
def proHard(request):
    request.encode="utf-8"
    response=''
    clg=ChangeLog.objects.all().order_by("-lasttime")
    clg=clg[0]
    tem_ctl=clg.tem
    hum_ctl=clg.hum
    pre_ctl=clg.pre
    led_ctl=clg.led
    tem_ctl_need=5-len(tem_ctl)
    hum_ctl_need=5-len(hum_ctl)
    led_ctl_need=5-len(led_ctl)
    pre_ctl_need=5-len(pre_ctl)
    a="0"
    for i in range(tem_ctl_need):
        tem_ctl=a+tem_ctl
    for i in range(led_ctl_need):
        led_ctl=a+led_ctl
    for i in range(pre_ctl_need):
        pre_ctl = a + pre_ctl
    for i in range(hum_ctl_need):
        hum_ctl = a + hum_ctl
    response +='t=' + tem_ctl + '&' + 'l=' + led_ctl + '&p=' + pre_ctl + '&h=' + hum_ctl
    #response+='_*_'+'t='+tem_ctl+'&'+'l='+led_ctl+'&p='+pre_ctl+'&h='+hum_ctl
    print(request)
    if request.method=='POST':
        txt=request.POST['text']
        print("get text:",txt)
        #处理文本数据并存库
        param_split=txt.split('&')
        param_t=param_split[0].split('=')[1]
        param_l=param_split[1].split('=')[1]
        param_p=param_split[2].split('=')[1]
        param_h=param_split[3].split('=')[1]

        vpm=ViewParam()
        vpm.tem=param_t
        vpm.led=param_l
        vpm.pre=param_p
        vpm.hum=param_h
        vpm.save()

    return HttpResponse(response)

def returnImage(request):
    dir='realtime_images'
    lists = os.listdir(dir)  # 列出目录的下所有文件和文件夹保存到lists
    print(list)
    lists.sort(key=lambda fn: os.path.getmtime(dir + "\\" + fn))  # 按时间排序
    file_new = os.path.join(dir, lists[-1])  # 获取最新的文件保存到file_new
    print(file_new)
    f=open(file_new,'rb')
    data=f.read()
    f.close()
    return HttpResponse(data,content_type="image/jpeg")

def proIncubator(request):
    res = {}  # 存储箱子的相关信息
    # 取出最早的一条数据
    Obj = ViewParam.objects.all().order_by('-lasttime')
    if Obj:
        Obj = Obj[0]
        res['tem_cur'] = Obj.tem
        res['hum_cur'] = Obj.hum
        res['pre_cur'] = Obj.pre
        res['led_cur'] = Obj.led
    else:
        pass
    if request.POST:
        clg = ChangeLog()
        clg.tem = request.POST['tem_ctl']
        clg.hum = request.POST['hum_ctl']
        clg.led = request.POST['led_ctl']
        clg.pre = request.POST['pre_ctl']
        clg.save()
        res['response'] = "修改已经收到：" + clg.tem
    return render(request, 'incubatorDetail2.html', res)

#用户初次使用系统流程
def guide(request):
    return render(request,'connectingGuide.html')
