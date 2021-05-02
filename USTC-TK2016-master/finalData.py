#-*- coding:utf-8 -*-
import numpy as np
#from PIL import Image
import binascii
import errno
import os
def getArrayfrom_pcap(filename):#####把切割好的pacp文件转换成矩阵，8位一个整数保存
    with open(filename, 'rb') as f:##以二进制形式打开filename'文件
        content = f.read()##打开是16进制
    hexst = binascii.hexlify(content)  #通过这个转化成16进制一维数组
    fh = np.array([int(hexst[i:i+2],16) for i in range(0, len(hexst), 2)])
    #然后通过将2个16进制的数字合并，组成一个不超过256的10进制，依旧是一维数组
    #到这一步我已经找到我需要的数据形式了，后面只是保存形式的不同而已
    return fh
def mkdir_p(path):
    try:
        os.makedirs(path)#在给定的path目录下创建目录，
        #os.makedirs('Desktop/toolkit/USTC-TK2016-master/3_ProcessedSession/TrimedSession/Train/test')这才是正确的语法
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


#%%

#path = 'C:/Users/dell/Desktop/Malware/'
#只对train文件运算？
path = '3_ProcessedSession/TrimedSession/Train/27-ALL'
count = 0
final = np.zeros((1,784))


with open('./test-malware.txt', 'ab') as f:##支持连续写入不覆盖
    for i,d in enumerate(os.listdir(path)):
        p = os.path.join(path,d)
        print(p)
        arr = getArrayfrom_pcap(p)###得到一维数组
        arr = np.expand_dims(arr, axis = 0)###变成二维，不然无法appendr
        count = count + 1
        final = np.append(final,arr,axis=0)
        ####final够五百就写入，然后清空
        if(count == 500):
            final = np.delete(final, 0, 0)
            np.savetxt(f,final)#将array写入txt文件
            final = np.zeros((1,784))#用0补充，清空
            count = 0
            print("write+1")
        else:
            continue
    if(count == 0):
        pass
    else:       #最后一点没有500个的时候
        final = np.delete(final,0,0)
        np.savetxt(f,final)
        print("write end")

