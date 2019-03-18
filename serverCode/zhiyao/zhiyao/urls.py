"""zhiyao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('incubator/',views.incubator,name='incubator'),
    path('bbs/',views.bbs,name='bbs'),
    path('incubatorDetail/<incubatorno>/',views.incubatorDeatil,name='incubatorDetail'),
    path('alterenviroment/<incubatorno>/',views.alterenviroment,name="alterenviroment"),
    path('bbs/',views.bbs,name="bbs"),
    path("bbs/writePurchase/",views.writePurchase),
    path("bbs/writePurchase/save/<userphone>",views.savePurchase),
    path('bbs/writeSelling/',views.writeSelling),
    path('bbs/writeSelling/save/<userphone>',views.saveSelling),
    path('bbs/writeCommunication',views.writeCommunication),
    path('bbs/writeCommunication/save/<userphone>',views.saveCommunication),
    path('getbbs/',views.getbbs),
    path('getbbs/purchaseDetail/<id>',views.getPDetail,name='pDetail'),
    path('getbbs/sellingDetail/<id>',views.getSDetail,name='sDetail'),
    path('getbbs/communicationDetail/<id>',views.getCDetail,name='cDetail'),
    path('my/',views.my),
    #############################路径需要修改
    path('guide', views.guide),
    path('', views.proIncubator),  # 处理来自网页的箱子控制信息,返回箱子参数信息web
    path('hard', views.proHard),  # 接收本地sock服务器转发的硬件相关数据
    path('image', views.returnImage),  # 由页面自动发起请求，获取箱内图片
]
