#!/usr/bin/env 
# -*- coding: utf-8 -*-

import sys
﻿import serial
import time

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
    global ser,repeat
    ser.write(c)
    while True:
        if ser.inWaiting () == 0:
            if repeat:
                ser.write(c)
                repeat -= 1
            else:
                print('Timeout!')
                return
        else:
            time.sleep(0.2)
            data = ser.read(ser.inWaiting())
            data = list(data)
            print('')
            print ('RX:',end=' ')

if __name__ == '__main__':
    global ser

    Pare = sys.argv[1]
    
    ser = serial.Serial()
    ser. parity='E'
    ser.port= '/dev/ttyUSB2'
    try:
        ser.open()
    except BaseException as e:
        print (e)
        
    with open('./'+Pare) as file:
        NumofLine = 1
        CommandArray = []
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
                    CommandArray += [Command]
            NumofLine += 1
    print(CommandArray)
    for i in CommandArray:
        if Test(i):
            print('Please press any key to exit')
            tmp = input()
            exit()




