#!/usr/bin/env
# -*- coding: utf-8 -*-

import sys
import time
import serial

def list2hex(l):
    t = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    s = ''
    for i in l:
        s = t[i>>4]+t[i&0xf]+' '

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
    tmp = len(a)+len(A)+7
    C = [0]
    L = [tmp>>8] + [tmp&0xff]
    HCS = Fcs(L+C+A)
    return [0x68]+L+C+A+HCS+a+[0,0]+Fcs(L+C+A+HCS+a+[0,0])+[0x16]

def Translate(s):
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
                return None , err
    if len(tmp)%2:
        return None,'The larg of command is incorrect'
    data = []
    i = 0
    while tmp[i:i+2]:
        data += [(tmp[i]<<4)+tmp[i+1]]
        i += 2
    return data,None

def Test(c):
    global SER,REPEAT,TIMEOUT   
    repeat = REPEAT
    tmp = ''
    while repeat+1:
        SER.write(c)
        tmp += "TX:"+ list2hex(c) + '\n'
        timeout = TIMEOUT
        while timeout:
            if SER.inWaiting () == 0:
                time.sleep(1)
                timeout -= 1
            else:
                time.sleep(0.2)
                data = SER.read(SER.inWaiting())
                data = list(data)
                tmp += "RX:" + list2hex(data) + '\n'
                return tmp,None
        repeat -= 1
    tmp += 'no responed \n'
    return None,tmp
            

if __name__ == '__main__':
    global SER,REPEAT,TIMEOUT,A
    A = [17,17,17,17,17,17]
    REPEAT = 2
    TIMEOUT = 15
    try:
        Para = sys.argv[1]
    except:
        print("Please check the parameter")
        exit()

    SER = serial.Serial()
    SER.parity='E'
    SER.port= '/dev/ttyUSB2'
    try:
        SER.open()
    except BaseException as e:
        print (e)
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
                    print('load the line ',NumofLine,Command)
                    CommandArray += [Command]
            NumofLine += 1

    for i in CommandArray:
        respones,err = Test(i)
        if err:
            print(err,'Please press any key to exit')
            tmp = input()
            exit()
        else:
            print(respones)
