def NULL(d):
    return 'None',d[1:]
def array (d):
    l = d[1]
    d = d[2:]
    a = []
    for i in range(l):
        tmp , d = data[d]
        a += [tmp]
    return a,d
def structure(d):
    l = d[1]
    d = d[2:]
    a = []
    for i in range(l):
        tmp , d = data[d]
        a += [tmp]
    return a,d
def bool(d):
    return d[1],d[2:]
def bit_string(d):
    pass
def double_long(d):
    s = 1
    if d[1] >0x7f:
        s = -1
    return s*(int((d[1]&0x7f)<<24)+int(d[2]<<16)+int(d[3]<<8)+int(d[4])),d[5:]
def double_long_unsigned(d):
    return int((d[1]&0x7f)<<24)+int(d[2]<<16)+int(d[3]<<8)+int(d[4]),d[5:]
def octet_string(d):
    l = d[1]
    d = d[2:]
    t = '0123456789ABCDEF'
    s = ''
    for i in range(l):
        s += t[d[i]>>4]+t[d[i]&0xf]
    return s,d[l:]
def visible_string(d):
    l = d[1]
    d = d[l:]
    s = ''
    for i in range(l):
        s += chr(d[i])
    return s,d[l:]
def UTF8_string(d):
    l = d[1]
    d = d[2:]
    t = '0123456789ABCDEF'
    s = ''
    for i in range(l):
        s += t[d[i]>>4]+t[d[i]&0xf]
    return s,d[l:]
def integer(d):
    if d[1] > 0x7f:
        return -(d[1]&0x7f),d[2:]
    else:
        return d[1]&0x7f,d[2:]
def long(d):
    if d[1] > 0x7f:
        return -(((d[1]&0x74)<<8)+d[2]),d[3:]
    else:
        return (d[1]<<8)+d[2],d[3:]
def unsigned(d):
    return d[1],d[2:]
def log_unsigned(d):
    return (d[1]<<8)+d[2],d[3:]
def long64(d):
    
'''

long64 [20],
long64-unsigned [21],
enum [22],
float32 [23],
float64 [24],
date_time [25],
date [26],
time [27],
date_time_s [28],
OI [80],
OAD [81],
ROAD [82],
OMD [83],
TI [84],
TSA [85],
MAC [86],
RN [87],
Region [88],
Scaler_Unit [89],
RSD [90],
CSD [91],
MS [92],
SID [93],
SID_MAC [94],
COMDCB [95],
RCSD [96]
'''
choice={0:NULL,1:array,2:structure,3:bool,4:bit_string,5:double_long}

def data(d):
    return choice(d[0])(d)
