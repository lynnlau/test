#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys,os,time,serial,configparser,re

class FunModule():
    def __init__(self,name):
        self.name = name
        self.items = []

def list2hex(l):
    t = '0123456789ABCDEF'
    s = ''
    for i in l:
        s += t[i>>4]+t[i&0xf]+' '
    return s

def Fcs(d):
    b=0
    v=0
    P=0x8408
    fcstab=[]
    fcs=0xffff
    for b in range(0,256):
        v=b;
        for i in range(0,8):
            v = (v >> 1) ^ P if v & 1 else v >> 1
        fcstab += [v]

    while d:
        fcs=(fcs >> 8) ^ fcstab[(fcs ^ d[0]) & 0xff]
        d = d[1:]
    fcs ^= 0xffff
    return [fcs&0xff]+[fcs>>8]

def Combine(a):
    global A
    tmp = len(a)+len(A)+9
    C = [0x43]
    SA = [5]
    CA = [0x10]
    L = [tmp&0xff] + [tmp>>8]
    HCS = Fcs(L+C+SA+A+CA)
    return [0x68]+L+C+SA+A+CA+HCS+a+Fcs(L+C+SA+A+CA+HCS+a)+[0x16]

def Analyze(d):
    try:
        while d[0]!=0x68:
            d = d[1:]
    except:
        return
    l = d[1]+(d[2]<<8)

    if len(d) < l+2:
        return False

    if d[l+1] != 0x16:
        return False
    '''
    if fcs16(d[1:l-1]) != d[l-1:l+1]:
        return False
    '''
    addrL = (d[4]&0xf)+1
    addr = d[4:addrL+5]
    '''
    if addr != A:
        return False
    '''
    apdu = d[addrL+8:]
    '''
    建立应用连接响应 [130] CONNECT-Response,
    断开应用连接响应 [131] RELEASE-Response,
    断开应用连接通知 [132] RELEASE-Notification,
    读取响应 [133] GET-Response,
    设置响应 [134] SET-Response,
    操作响应 [135] ACTION-Response,
    上报通知 [136] REPORT-Notification,
    代理响应 [137] PROXY-Response,
    异常响应 [238] ERROR-Response
'''
    if  apdu[0] == 133:
        pass
    elif  apdu[0] == 134: #SET-Response
        pass
    elif  apdu[0] == 135: #ACTION-Response
        pass
    elif  apdu[0] == 0:
        pass
    elif  apdu[0] == 0:
        pass
    else:
        pass

    print(apdu)

def Check(file):
    NumofLine = 0
    CommandArray = []
    while True:
        NumofLine += 1
        tmp = file.readline()
        if not tmp:
            return CommandArray,None
        while tmp[0] == ' ':
            tmp = tmp[1:]
        if tmp[:5] in ['wait ','judge','report','测试目的：','预期结果：']:
            CommandArray += [tmp]
        elif tmp == '\n':
            pass
        elif tmp =='':
            break
        else:
            l = ''
            for i in tmp:
                if i ==' ':
                    pass
                elif i == '\n':
                    break
                elif i not in '1234567890abcdefABCDEF':
                    return None,'line'+str(NumofLine)+'The content of APDU is incorrect'
                else:
                    l += i
            if len(l)%2:
                return None,'line'+str(NumofLine)+'The larg of APDU is incorrect'
            else:
                tmp = []
                while l:
                    tmp += [int(l[:2],16)]
                    l = l[2:]
                CommandArray += [tmp]
    return CommandArray,None


def compose (m,f=None):
    print(m)
    if f:
        with open(f,'a') as file:
            file.write( m )
            file.close()


def Send(m):
    global SER,REPEAT,TIMEOUT
    repeat = REPEAT
    SData = Combine(m)
    while repeat+1:
        SER.write(SData)
        print(time.time(),"TX:"+ list2hex(SData))
        timeout = TIMEOUT
        while timeout:
            if SER.inWaiting () == 0:
                time.sleep(1)
                timeout -= 1
            else:
                time.sleep(0.2)
                RData = SER.read(SER.inWaiting())
                RData = list(RData)
                print(time.time(),"RX:" + list2hex(RData))
                return RData,None
        #print(SER.read(1024))
        repeat -= 1
    return None,1

def Translate(c):
    return '未解析\n'

def judge(c):
    if re.match('\s+ok\s+',c):
        return 

def Test(l):
    log=''
    for c in l:
        if isinstance(c,list):
            log += Translate(c)
            rdata,err=Send(c)
            if err:
                log +=  '通信超时'
                return log,'通信超时'
        else:
            if c[:4] == 'wait':
                wait=''
                c=c[4:]
                i = 0
                while c[i:]:
                    if c[i] in '1234567890':
                        wait += c[i]
                    i += 1
                wait = int(wait)
                log += '等待' + str(wait) + '秒\n'
                while wait:
                    sys.stdout.write(' wait {0}s\r'.format(wait))
                    sys.stdout.flush()
                    time.sleep(1)
                    wait -= 1
                    sys.stdout.write(' ' * 10 + '\r')


            elif c[:5] == 'judge':
                log += '判断'

            elif c[:5] == 'report':
                log += 'raport'
            elif c[:4] == '测试目的':
                log += c
            elif c[:4] == '预期结果':
                log += c
            else:
                pass
    return log,None

def Exe(f):
    for m in f:
        funname = m.name
        compose(funname)
        items = m.items
        for i in items:
            try:
                file = open(funname+'/'+i)
            except BaseException as err:
                print(err)
                exit()

            command,err = Check(file)
            file.close()
            if err:
                print('in',funname,'>>',i)
                print(err)
                exit()
            else:
                compose(i)
                m,err = Test(command)
                if err:
                    print(err)
                    print(m)
                    s = input()
                    exit()
                else:
                    compose(m)


if __name__ == '__main__':
    global SER,REPEAT,TIMEOUT,A
    A = [17,17,17,17,17,17]
    REPEAT = 1
    TIMEOUT = 10
####开串口####
    l = os.popen("ls /dev |grep ttyUSB").read()
    tmp = ''
    array = []
    for i in l:
        if i == '\n':
            array += [tmp]
            tmp = ''
        else:
            tmp += i
    tmp = 0
    l = ''
    for i in array:
        print(tmp,': ',i)
        l+=str(tmp)
        tmp += 1
    i = input('Please change the num of serial: ')
    while i not in l:
        i = input('Please rechange the num of serial: ')
    print( array[int(i)])
    SER = serial.Serial()
    SER.parity='E'
    SER.port= '/dev/'+array[int(i)]#'/dev/ttyUSB0'
    try:
        SER.open()
    except BaseException as e:
        print (e)
        exit()

####打开测试清单####
    conf = configparser.ConfigParser()
    conf.read('example.ini')

    FunModules = conf.sections()
   #print('获取配置文件所有的section', projectes)
    '''
    options = conf.options(sections[0])
    print('获取指定section下所有option', options)
    items = conf.items(sections[0])
    print('获取指定section下所有的键值对', items)

    value = conf.get(sections[0],'1')
    print('获取指定的section下的option', type(value), value)
    '''
    FunModuleList = []
    for Fun in FunModules:
        f = FunModule(Fun)
        items = conf.options(Fun)
        for item in items:
            f.items += [conf.get(Fun,item)]
            '''
            with open(project+'/'+conf.get(project,item)) as file:
                print('load the command >>',project,'>>',conf.get(project,item))
                command,err = Translate(file)
                if err:
                    print('in',project,'>>',conf.get(project,item))
                    print(err)
                    exit()
                else:
                    P += command
             '''
        FunModuleList += [f]
    Exe(FunModuleList)
