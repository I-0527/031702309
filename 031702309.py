#coding=utf-8
import json
import string
import re
import cpca
import pandas as pd
import numpy as np
import git
def en_json(ob):              #编码为JSON类型
    result = json.dumps(ob,ensure_ascii=False)
    return result
    
def five_address(ob):          #ob为一个字符串
    d = {"姓名": '',
         "手机": '',
         "地址":[ '','','','','']
         }
    ob = ob.split(",")            #分割名字
    d["姓名"] = ob[0]
    ob = ob[1]  
    l = len(ob)
    ob = ob.split(".")
    ob = ob[0]                    #地址+手机号的混合
    num = re.findall(r"\d+",ob)   #提取手机号
    i=0
    while 1 :
        if i >= len(num) :
            break
        elif len(num[i]) == 11 :
            break
        else:
            i = i+1
    d["手机"] = num[i]
    ob = re.sub(d["手机"],"",ob)   #纯地址
    ob = ob.split()
    ob = cpca.transform(ob)        #划分四级地址
    address = np.array(ob)
    address = address[0]
    i=0
    while 1:
        d["地址"][i] = address[i]
        i = i +1
        if i >=3 :
            break
    if d["地址"][0][2] == "市" :
        d["地址"][0] = d["地址"][0][:2]
    address = address[3]           #查找第四级
    i = 0
    while 1:
        if address[i]=="镇":
            d["地址"][3] = address[:(i+1)]
            d["地址"][4] = address[(i+1):]
            break
        elif address[i]=="乡":
            d["地址"][3] = address[:(i+1)]
            d["地址"][4] = address[(i+1):]
            break
        elif address[i]=="街" and address[i+1]=="道" :
            d["地址"][3] = address[:(i+2)]
            d["地址"][4] = address[(i+2):]
            break
        elif i>=(len(address)-1) :
            d["地址"][4] = address
            break
        else :
            i = i+1
    return d

def seven_address(ob):
    ob = five_address(ob)
    d = ob['地址'][4]
    print(d)
    i = 0
    while 1:                      #查找街|路|巷
        if(d[i]=="路"or d[i]=='巷' or d[i]=='街'):
           ob['地址'][4] = d[:(i+1)]
           ob['地址'].append(d[(i+1):])
           break
        elif i>=len(d) :
           break
        else :
           i = i+1
    if(i>=len(d)):
           ob['地址'].insert(4,'')
    d = ob["地址"][5]
    i=0
    while 1:
        if d[i]=='号' :
           ob['地址'][5] = d[:(i+1)]
           ob['地址'].append(d[(i+1):])
           break
        elif i>=len(d):
           break
        else :
           i = i+1
    if(i>=len(d)):
           ob['地址'].insert(5,'')
    return ob


a = input().split("!")
if(a[0]=='1'):
    print( en_json(five_address(a[1])) )
elif (a[0] =='2'):
    print( en_json(seven_address(a[1])) )
else :
    print( en_json(seven_address(a[1])) )
