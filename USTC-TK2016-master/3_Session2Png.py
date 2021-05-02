# -*- coding: utf-8 -*-
# Wei Wang (ww8137@mail.ustc.edu.cn)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file, You
# can obtain one at http://mozilla.org/MPL/2.0/.
# ==============================================================================
#完成第三步图像生成
#numpy来存储较大的数组
#PIL库支持图像存储、显示和处理,pillow替代了PIL
import numpy
from PIL import Image
import binascii
import errno    
import os

PNG_SIZE = 28

def getMatrixfrom_pcap(filename,width):
    with open(filename, 'rb') as f:   #with as简化try finally语句
        content = f.read()
    hexst = binascii.hexlify(content)  #二进制数据转换十六进制
    fh = numpy.array([int(hexst[i:i+2],16) for i in range(0, len(hexst), 2)])  #创建数组，按字节分割，两个十六进制数为一字节，int(hex,16)将十六进制数转为int类型
    rn = int(len(fh)/width)
    fh = numpy.reshape(fh[:rn*width],(-1,width))  #？？？
    fh = numpy.uint8(fh)
    return fh

#递归创建多级目录
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

paths = [['3_ProcessedSession/TrimedSession/Train', '4_Png/Train'],['3_ProcessedSession/TrimedSession/Test', '4_Png/Test']]
for p in paths:
    for i, d in enumerate(os.listdir(p[0])):#os.listdir返回指定文件夹包含的文件或文件夹名列表,因为只有一个文件夹，所以i=0
        dir_full = os.path.join(p[1], str(i))#路径拼接4_Png/Train
        mkdir_p(dir_full)
        for f in os.listdir(os.path.join(p[0], d)):#遍历3_ProcessedSession/TrimedSession/Train/BitTorrent-L7中的文件
            bin_full = os.path.join(p[0], d, f)
            im = Image.fromarray(getMatrixfrom_pcap(bin_full,PNG_SIZE))#将矩阵转化为图像
            png_full = os.path.join(dir_full, os.path.splitext(f)[0]+'.png')
            im.save(png_full)
