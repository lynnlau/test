#!/usr/bin/env
# -*- coding: utf-8 -*-
def Get_Response(a):
    '''
    1 读取一个对象属性的响应
    2 读取若干个对象属性的响应
    3 读取一个记录型对象属性的响应
    4 读取若干个记录型对象属性的响应
    5 分帧响应一个数据块
    6 读取一个对象属性的 MD5 值的响应

    GetResponseNormal,
    GetResponseNormalList,
    GetResponseRecord,
    GetResponseRecordList,
    GetResponseNext,
    GetResponseMD5
    '''
    a = a[1:]
    if a[0]==1:
        if a[6]:
            return data(a[6:])
        else:
            return False,a[7:]
    elif a[0]==2:
        n = a[1]
        a = a[2:]
        result = []
        for i in range(n):
            tmp,a = data[a]
            result += [tmp]
        return result,a
    elif a[0]==3:
        n = a[6]
        a = a[7:]
        result = []
        for i in range(n):
            a=a[5:]
        if a[0]:
            n = a[1]
            a = a[2:]
            for i in range(n):
                tmp , a = data(a)
                result += [tmp]
            return result,a
       else:
           return False,a



def SET_Response(a):
    a = a[1:]
    if a[0]==1:
        pass
    elif a[0]==2:
        pass
    elif a[0]==3:
        pass
    else:
        return
def Analyze(m):
    try:
        while m[0]!=0x68:
            m = m[1:]
    except:
        return
    l = m[1]+(m[2]<<8)

    if len(m) < l+2:
        return False

    if m[l+1] != 0x16:
        return False
    '''
    if fcs16(d[1:l-1]) != d[l-1:l+1]:
        return False
    '''
    addrL = (m[4]&0xf)+1
    addr = m[4:addrL+5]
    '''
    if addr != A:
        return False
    '''
    apdu = m[addrL+8:]
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
        return Get_Response(apdu)
    elif  apdu[0] == 134: #SET-Response
        return SET_Response(apdu)
    elif  apdu[0] == 135: #ACTION-Response
        pass
    elif  apdu[0] == 0:
        pass
    elif  apdu[0] == 0:
        pass
    else:
        pass

    print(apdu)
