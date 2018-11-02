#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys
import time
import serial

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
    if apdu[0] == 133:
        pass
    elif  apdu[0] == 134: #SET-Response
    elif  apdu[0] == 135: #ACTION-Response
        pass
    elif  apdu[0] == :
        pass
    elif  apdu[0] == :
        pass
    else:
        pass
        
    print(apdu)

def Translate(s):
    i = 0
    while s[i]==' ':
        i+=1
    s = s[i:]

    tmp = []
    for i in s:
        if i == ' ':
            pass
        elif i == '\n':
            break
        else:
            try:
                tmp += [int(i,16)]
            except BaseException as err:
                return s , None
    if len(tmp)%2:
        return None,'The larg of APDU is incorrect'
    data = []
    i = 0
    while tmp[i:i+2]:
        data += [(tmp[i]<<4)+tmp[i+1]]
        i += 2
    return data,None

def Test(c):
    global DATA
    if isinstance(c,list):
        global SER,REPEAT,TIMEOUT   
        repeat = REPEAT
        SData = Combine(c)
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
                    result,data = Analyze(RDate)
                    if result:
                        DATA = data
                        print(result)
                        return result,None
                    else:
                        return None,data 
            repeat -= 1
        return None,'no responed \n'
    else: 
        if not c:
            return None,None
        if c[:4] == 'wait':
            wait=''
            c=c[4:]
            i = 0
            while c[i:]:
                if c[i] in '1234567890':
                    wait += c[i]
                i += 1
            wait = int(wait)
            tmp = 'wait '+wait+' s\n'
            while wait:
                sys.stdout.write(' wait {0}s\r'.format(wait))
                sys.stdout.flush()
                time.sleep(1)
                wait -= 1
                sys.stdout.write(' ' * 10 + '\r')
            tmp += 'end the waiting'
            return tmp,None

        elif c[:5] == 'judge':
            return s,None
        else:
            pass



if __name__ == '__main__':
    global SER,REPEAT,TIMEOUT,A
    A = [17,17,17,17,17,17]
    REPEAT = 2
    TIMEOUT = 15

    SER = serial.Serial()
    SER.parity='E'
    SER.port= '/dev/ttyUSB0'
    try:
        SER.open()
    except BaseException as e:
        print (e)
        exit()
    try:
        open('./CommadTask') as file:
    except:
        print('')
        exit()
    
    with open('./'+Para) as file:
        NumofLine = 1
        CommandArray = []
        print('load the command...')
        while True:
            tmp = file.readline()
            if tmp == '':
                break
            elif tmp =='\n':
                pass
            else:
                Command ,err = Translate(tmp)
                if err:
                    print('line',NumofLine,': invalid command in identifier')
                    print('information:',err)
                    print('Please press any key to exit')
                    tmp = input()
                    exit()
                elif Command == None:
                    pass
                else:
                    try:
                        print('load the line',NumofLine,':',list2hex(Command))
                        CommandArray += [Command]
                    except:
                        print('load the line',NumofLine,':',Command,end='')
                        CommandArray += [Command]
            NumofLine += 1
    
    print('loading is completed!')
    print('''
    
    ''')
    
    for i in CommandArray:
        respones,err = Test(i)
        if err:
            print(err,'Please press any key to exit')
            tmp = input()
            exit()
        else:
            print(respones)
