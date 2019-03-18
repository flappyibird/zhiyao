import network,myModules2
import time,sensor

#服务器ip和端口号
serverIP = '192.168.43.36'
serverPort1 = 8081
#ap热点名称和密码
apname = 'zhiyao'
appass = '1234567890'
#存储从arduino得到的数据,初始时置为一个默认值
ardbuf="t=15.00&l=10000&p=100000&h=40.00"
#存储从服务器得到的消息
serbuf=""
# Reset sensor
sensor.reset()
# Set sensor settings
sensor.set_contrast(1)
sensor.set_brightness(1)
sensor.set_saturation(1)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.QQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)
while True:
    try:
        fo = myModules2.fileOperate()
        if not fo.isconnectWIFI():
            print("用户信息失效")
            print("启动HTTP服务器:192.168.1.1:8080")
            httpserver = myModules2.httpServer(apname,appass)
            httpserver.runserver()
            info = httpserver.getUserInfo()
            fo.updateInfo(info)
            print("用户信息已更新")
        else:
            while True:
                try:
                    info = fo.getInfo()
                    print("连接WIFI。")
                    wifi = myModules2.wifiControl(info)
                    print("启动相机模块")
                    #pho=myModules2.camera()
                    print("启动套接字。")
                    cli=myModules2.clientSOCK(serverIP,serverPort1)
                    #参数服务器地址
                    serverinfo1=[serverIP,serverPort1]
                    #验证用户手机号和箱子id，以后补上：
                    #
                    while True:
                        clock=time.clock()
                        clock.tick()
                        #===========================================
                        #服务器交互过程
                        #===========================================
                        #获取一张图片,返回IMAGE类对象
                        #img=pho.getImage()
                        frame = sensor.snapshot()
                        img = frame.compressed(quality=35)
                        #ardbuf是arduino返回的消息
                        #数据格式："t=2.2&l=5&p=6&h=2.2"
                        #"t=xx.xx&l=xxxxx&p=xxxxxx&h=xx.xx"
                        #
                        #serbuf是服务器返回的消息
                        #发送图片消息
                        cli.send(img,2)
                        print("get response:",serbuf)
                        #发送文本消息
                        serbuf=cli.send(ardbuf,1)
                        #============================================
                        #arduino交互过程
                        #============================================
                        ardbuf=""
                        # 读arduino
                        #！！！！！！！！！serbuf可能需要处理一下
                        print("来自服务器的反馈：",serbuf)
                        ardpro=myModules2.arduinoPro(serbuf)
                        tmp = b''#收到的arduino传感器参数
                        tmp +=ardpro.sendAndReiceive()
                        if tmp == None:
                           print("get None.")
                        ardbuf+=tmp.decode()
                        print("来自arduino:", ardbuf)
                except myModules2.myError as e:
                    print("moduleerror:",e)
                    fo.updateInfo(e.getInfo())
                #这一块曾导致了莫名其妙的bug,以后出了问题请把下面的except删掉

    except myModules2.myError as e:
        print(e)



