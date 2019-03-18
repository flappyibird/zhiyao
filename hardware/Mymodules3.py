'''
1.http服务器，处理http请求并获取用户信息
2.文件操作，读取用户信息，连接WIFI，更新用户信息
    文件格式：wifi,password,phone,
3.myError异常, 当用户信息无效时被抛出，当无法连接WiFi时抛出
4.客户端，连接wifi,发送消息，接收消息
5.arduino连接，发送arduino消息，接收arduino消息
6.摄像模块，启动摄像头，捕获mjpeg流信息并发送
7.WIFI,根据给定信息连接WIFI
8.发送Get请求，接收响应消息
9.给arduino发送控制消息，从arduino 接收当前传感器参数
11.使用套接字发送数据
'''
import socket,re,network,sensor,image,time,pyb,ustruct,usocket
from pyb import UART

#箱子ID
incubatorid = "123456"

index_content = '''
HTTP/1.x 200 ok
Content-Type:text/html


'''
file = open('index.html', 'r')
index_content += file.read()
file.close()

# read reg.html, put into HTTP response data
reg_content = '''
HTTP/1.x 200 ok
Content-Type:text/html


'''
file = open('reg.html', 'r')
reg_content += file.read()
file.close()

#1.
class httpServer:
    # read index.html,put into HTTP response data
    # __index_content='''
    # HTTP/1.x 200 ok
    # Content-Type:text/html
    #
    #
    # '''
    # #reg html
    # __reg_content = '''
    #     HTTP/1.x 200 ok
    #     Content-Type:text/html
    #
    #
    # '''
    wifi=''
    password=''
    phone=''
    __HOST = ''  # Use first available interface
    __PORT = 8080  # Arbitrary non-privileged port
    apname = ''
    appass = ''
    def __init__(self,apname,appass):
        #读入html数据，并加入HTTP响应数据中
        # file = open('index.html','r')
        # self.__index_content += file.read()
        # file.close()
        # file=open('reg.html','r')
        # self.__reg_content+=file.read()
        # file.close()
        self.apname = apname
        self.appass = appass

    def runserver(self):
        wlan = network.WINC(mode=network.WINC.MODE_AP)
        wlan.start_ap(self.apname, key=self.appass, security=wlan.WEP, channel=2)
        print("热点已启动：",self.apname,self.appass)
        while True:
            # Create server socket
            print("启动服务器套接字")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                # Bind and listen
                s.bind([self.__HOST, self.__PORT])
                s.listen(100)
                # Set server socket timeout
                # NOTE: Due to a WINC FW bug, the server socket must be closed and reopened if
                # the client disconnects. Use a timeout here to close and re-create the socket.
                s.settimeout(100)
                print("启动服务处理程序：")
                self.processHTTP(s)
                print("正常关闭socket套接字")
                s.close()
                break
            except OSError as e:
                s.close()
                print("http:socket error: ", e)

    def processHTTP(self,s):
        # infinite loop until get id and key
        jumpout = 0
        while jumpout == 0:
            conn, addr = s.accept()
            request = conn.recv(1024)
            if len(request) == 0:
                conn.close()
                print("a bad girl")
                continue
            method = request.decode('utf-8').split(' ')[0]
            src = request.decode('utf-8').split(' ')[1]

            print('Connect by:', addr)
            print('Request is:\n', request)

            # deal with GET method
            if method == 'GET':
                if src == '/index.html':
                    # content = self.__index_content
                    content = index_content
                elif src == '/reg.html':
                    # content = self.__reg_content
                    content = reg_content
                elif re.match('^/\?.*$', src):
                    entry = src.split('?')[1]  # main content of the request
                    content = 'HTTP/1.x 200 ok Content-Type: text/html\r\n\r\n'
                    content += entry
                    content += '<br/><font color="green" size="7">register success!</p>'
                else:
                    conn.close()
                    print("get invalid info")
                    continue

            # deal with POST method
            elif method == 'POST':
                print("get post:")
                form = request.decode('utf-8').split('\r\n\r\n')
                entry = form[-1]  # main content of the request
                content = 'HTTP/1.x 200 ok \r\nContent-Type:text/html\r\n\r\n'
                content += entry
                content += '<br/><font color="green" size="7">register Sucess!</p>'
                #print(entry)
                entryarray = entry.split('\r\n')
                apname = entryarray[0].split('=')[1]
                appass = entryarray[1].split('=')[1]
                usphone = entryarray[2].split('=')[1]
                self.wifi = apname
                self.password = appass
                self.phone = usphone
                print(apname, appass, usphone)
                jumpout = 1  # 设定结束循环

            ####
            # More operations, such as put the form into database
            ####

            else:
                conn.close()
                print("unexpected error")
                continue
            print("http返回响应：",content)
            conn.send(content.encode('utf-8'))
            # close connection
            conn.close()

    def getUserInfo(self):
        info=[self.wifi,self.password,self.phone]
        return info

#2.
class fileOperate:
    wifi=''
    password=''
    phone=''

    def __init__(self):
        with open('info.txt','r') as file:
            content = file.read()
        info = content.split(',')
        if 1==len(info):
            self.wifi = ""
            self.password = ""
            self.phone = ""
        else:
            self.wifi=info[0]
            self.password=info[1]
            self.phone=info[2]
        file.close()

    def isconnectWIFI(self):
        if len(self.wifi)!=0:
            wlan = network.WINC()
            wlan.connect(self.wifi, key=self.password, security=wlan.WPA_PSK)
            sta = wlan.isconnected()
            if sta:
                print(wlan.ifconfig())
                wlan.disconnect()
                return True
            else:
                return False
        return False

    def getInfo(self):
        return [self.wifi,self.password,self.phone]

    def updateInfo(self, info):
        self.wifi=info[0]
        self.password=info[1]
        self.phone=info[2]
        # with open('info.txt','w') as file:
        #     file.write(info[0])
        #     file.write(',')
        #     file.write(info[1])
        #     file.write(',')
        #     file.write(info[2])
        #     file.write(',')
        file = open('info.txt','w')
        file.write(info[0])
        file.write(',')
        file.write(info[1])
        file.write(',')
        file.write(info[2])
        file.write(',')
        file.close()


#3
class myError(Exception):
    def __init__(self,value,info=''):
        self.value = value
        self.info = info

    def __str__(self):
        if 0 == self.value:
            return "invalid user info"
        if 1 == self.value:
            return "WiFi disconnected"

    def getInfo(self):
        return self.info

#4
class tcpClient:
    __head = 'head'
    __type0 = 'invalidif'
    __type1 = 'parameter'
    __content = ''
    __end = 'end'
    __segsig = '#'
    __consig = ','
    __buf = ''#存储接收到的数据
    def __init__(self,info,server,timeout=10):
        self.__serverIP = server[0]
        self.__serverPort = server[1]
        self.incubator = incubatorid
        # self.wifi = info[0]
        # self.password = info[1]
        self.phone = info[2]
        # self.wlan = network.WINC()
        # self.wlan.connect(self.wifi, key=self.password, security=self.wlan.WPA_PSK)
        # if not self.wlan.isconnected():
        #     raise myError(1)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client.settimeout(timeout)

    def __del__(self):
        self.close()

    def connect(self):
        #苦于不知道使用什么样的办法来判断是否连接成功，这里暂时不做处理，交由外部的异常捕获机制处理
        self.client.connect((self.__serverIP, self.__serverPort))
        print("正在连接...")
        return True

    def send(self,content):
        message = ''
        message += self.__head
        message += self.__segsig
        message += self.__type1
        message += self.__segsig
        message += content
        message += self.__segsig
        message += self.__end
        self.client.send(message)

    def sendImage(self,image):
        self.client.send(image)

    def sendFirst(self):
        message = ''
        message += self.__head
        message += self.__segsig
        message += self.__type1
        message += self.__segsig
        message += "id0="
        message += self.incubator
        message += self.__consig
        message += "id1="
        message += self.phone
        message += self.__consig
        message += self.__segsig
        message += self.__end
        self.client.send(message)

    def recv(self,size=1024):
        return self.client.recv(size)

    def close(self):
        self.client.close()

5
class arduinointer:
    def __init__(self):
        self.uart = UART(3,115200)

    def send(self,conarr):
        ardinf = '{'
        for i in conarr:
            ardinf += conarr[0]
            ardinf += ' '
        ardinf += '}}'
        self.uart.write(ardinf+'\n')

    def recv(self):
        return self.uart.read()

#6
class camera:
    def __init__(self):
        # Reset sensor
        sensor.reset()
        # Set sensor settings
        sensor.set_contrast(1)#设置对比度
        sensor.set_brightness(1)#设置亮度
        sensor.set_saturation(1)#设置饱和度
        sensor.set_gainceiling(16)#设置相机图像增益上限
        sensor.set_framesize(sensor.QQVGA)#设置帧大小
        sensor.set_pixformat(sensor.GRAYSCALE)#设置像素模式
        #sensor.skip_frames(time = 2000)     # Wait for settings take effect.

    def getImage(self):
        frame = sensor.snapshot()
        cframe = frame.compressed(quality=50)
        #print(type(cframe))
        return cframe

#7
class wifiControl:
    def __init__(self,info):
        self.wifi = info[0]
        self.password = info[1]
        self.phone = info[2]
        self.wlan = network.WINC()
        self.wlan.connect(self.wifi, key=self.password, security=self.wlan.WPA_PSK)
        if not self.wlan.isconnected():
            raise myError(1)

    def isconnected(self):
        if not self.wlan.isconnected():
            return False
        else:
            print(self.wlan.ifconfig())
            return True

#8
class clientHTTP:
    port = 8080
    path = '/hard'
    host = '127.0.0.1'
    requestUrl = 'GET %s HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36\r\nAccept: */*\r\n\r\n'
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
    #先发送消息，然后等待接收，返回服务器响应的消息
    def socket(self,content):
        self.path+='?'
        self.path+=content
        self.sock.send((requestUrl % (self.path, self.host)).encode())
        response = b''
        rec = sock.recv(1024)
        while rec:
            response += rec
            rec = sock.recv(1024)
        data=response.decode()
        data=data.split("_*_")
        return data[1]

#9
class arduinoPro:
    def __init__(self, content):
        self.text=content;
        self.data=ustruct.pack("<%ds" % len(self.text), self.text)
        self.buf=""
        self.bus=pyb.I2C(2,pyb.I2C.SLAVE,addr=0x12)
        self.bus.deinit()#完全关闭设备
        self.bus=pyb.I2C(2,pyb.I2C.SLAVE,addr=0x12)

    def sendAndReiceive(self):
        print("wait for arduino!")
        isrecv=0
        while (True):
            try:
                self.bus.send(ustruct.pack("<h", len(self.data)), timeout=10000)  # 首先发送长度 (16-bits).
                try:
                    self.bus.send(self.data, timeout=10000)
                    print("Send Data!")
                except OSError as err:
                    pass
            except OSError as err:
                pass
            try:
                buf1 = self.bus.recv(32, timeout=10000)
                print(buf1)
                return buf1
            except OSError as err:
                pass
#10
class mjpegPro:
    port=8080
    host='192.168.43.36'
    path='/mjpeg'
    requestUrl='GET %s HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36\r\nAccept: */*\r\n\r\n'

    def __init__(self):
        self.sock=usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        print("连接成功：")

    def send(self,content):
        self.sock.send(content)

#11
class clientSOCK:

    def __init__(self,host,port):
        self.host=host
        self.port=port
        self.sock=usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)
        self.sock.connect((self.host,self.port))
        print("连接成功")
    def send(self,content,op):
        #发送文本消息
        if op==1:
            self.sock.send(content)
            #确认收到
            self.sock.send("|*text*|")
            recv=self.sock.recv(1024)
            print("txt")
            res=recv.decode()
            print("I have message:",res)
            return res
        #发送图片消息
        if op==2:
            self.sock.send(content)
            self.sock.send("|*graph*|")
            recv=self.sock.recv(1024)
            print("graph")
            return
        return



