#coding:utf8
import json
from locale import atoi

from django.shortcuts import render
import subprocess
import dpkt
import socket
import collections
import time
from upfile.models import FlowFeature,Features,SessionFeatures
from django.http import HttpResponse, JsonResponse
try:
    import scapy.all as scapy
except ImportError:
    import scapy
try:
    # This import works from the project directory
    import scapy_http.http
except ImportError:
    # If you installed this package via pip, you just need to execute this
    from scapy.layers import http
# Create your views here.

import os



featurelists = []
filedir= []
sessionlist = []
flowlist = []
filename = []
def index(request):
    return render(request,'upfile/index.html'
                  )

def showsession(request):
    return render(request, "upfile/showsession.html")


def test1(request):
    return render(request, "upfile/test1.html")
def test(request):
    return render(request, "upfile/test.html")
def upfilemodel(request):
    return render(request,'upfile/upfilemodel.html')
def composeflow(request):
    return render(request,'upfile/composeflow.html')

def composesession(request):
    return render(request,'upfile/composesession.html')

# def upfile(request):
#     if request.method == "POST":
#         files = request.FILES.getlist("pcapfile", None)
#         if files is None:
#             return HttpResponse("没有文件")
#         else:
#             path = 'USTC-TK2016-master/1_Pcap'
#             project_path = os.path.abspath(os.getcwd()) + '/'
#             for file in files:
#                 dir_file = os.path.join(project_path, path, file.name)#文件存储路径包括文件名
#                 filedir.append(dir_file)
#                 with open(dir_file, 'wb+') as f:
#                     for chunk in file.chunks():
#                         f.write(chunk)
#             print("文件写入成功")
#         return render(request,'upfile/showfeature.html',
#                       {
#                           'message':'文件上传成功',
#                       }
#                       )
#     return render(request,'upfile/showfeature.html',
#                   {
#                       'message':'文件上传失败',
#                     }
#                   )
#点击按钮时触发的事件，完成文件保存，特征提取传送到showfeature显示出特征

def getfeatures(request):
    # 上传文件
    global featurelists
    featurelists = []
    global filedir
    filedir= []
    global sessionlist
    sessionlist = []
    global flowlist
    flowlist = []
    global filename
    filename = []
    print("111")
    if request.method == "POST":
        files = request.FILES.getlist("pcapfile", None)
        if files is None:
            return render(request, 'upfile/upfilemodel.html',
                          {'message': '上传失败',
                           }
                          )
        else:
            path = 'USTC-TK2016-master/1_Pcap'
            project_path = os.path.abspath(os.getcwd()) + '/'
            for file in files:
                dir_file = os.path.join(project_path, path, file.name)#文件存储路径包括文件名
                filedir.append(dir_file)
                filename.append(file.name)
                with open(dir_file, 'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
            print("文件写入成功")

        f = open(filedir[-1], 'rb')
        pcap = dpkt.pcap.Reader(f)
        src = []
        dst = []
        srcport = []
        dstport = []
        proto = []
        for (ts, buf) in pcap:  # ts为每条记录的时间戳，buf存放对应的包
            feature = {}
            fea = {}
            eth = dpkt.ethernet.Ethernet(buf)  # 第一层剥离，除去物理层，得到链路层
            ip = eth.data  # 二层剥离 得到网络层 此层可得到ip源地址，目的地址
            tcp = ip.data  # 第三层 得到传输层，可根据此层得到端口号，

            strtime = str(ts)
            strlist = strtime.split('.')
            dateArray = time.localtime(atoi(strlist[0]))
            datetime = time.strftime("%Y/%m/%d %H:%M:%S", dateArray)
            lasttime = datetime + "." + strlist[1][0:6]  # 不加切割会数据出现格外的几位数
            feature['time'] = lasttime
            feature['date'] = ts
            feature['src'] = socket.inet_ntoa(ip.src)  # 将网络地址转换成“.”点隔的字符串格式
            feature['dst'] = socket.inet_ntoa(ip.dst)
            feature['srcport'] = tcp.sport  # 端口号在传输层，tcp是传输层协议
            feature['dstport'] = tcp.dport
            feature['proto'] = ip.get_proto(ip.p).__name__  # 获得协议

            fea['timestamp'] = lasttime
            fea['time'] = ts
            fea['src'] = socket.inet_ntoa(ip.src)  # 将网络地址转换成“.”点隔的字符串格式
            fea['dst'] = socket.inet_ntoa(ip.dst)
            fea['srcport'] = tcp.sport  # 端口号在传输层，tcp是传输层协议
            fea['dstport'] = tcp.dport
            fea['proto'] = ip.get_proto(ip.p).__name__  # 获得协议
            Features.objects.create(fea)

            # 时间戳转化为时间
            # dateArray = time.localtime(ts)
            # date = time.strftime("%Y/%m/%d %H:%M:%S", dateArray)

            src.append(feature['src'])
            dst.append(feature['dst'])
            srcport.append(feature['srcport'])
            dstport.append(feature['srcport'])
            proto.append(feature['proto'])
            featurelists.append(feature)
        f.close()
        print("分析成功")
        print(featurelists[0])
        return render(request,'upfile/upfilemodel.html',
                      {'message':'上传成功',
                       }
                      )
    else:
        return render(request, 'upfile/upfilemodel.html',
                      {'message': '上传失败',
                       }
                      )
#用法scapy的方式得到特征，用与按流，按会话切割
def getfeatures1(str):
    dic = {}
    packets = scapy.rdpcap(str)
    if packets:
        dic["dst"] = packets[0][1].dst
        dic["src"] = packets[0][1].src
        dic["sport"] = packets[0][1].sport
        dic["dport"] = packets[0][1].dport
        dic["proto"] = packets[0][1].proto
        return dic
#为了解决刷新页面特征列表为空

# 数组版
# def showfeature(request):
#     #  读取分析文件
#     if featurelists:
#         print('yeyeyeyye')
#         return render(request,'upfile/showfeature.html',
#                       {
#                           'featurelists':featurelists,
#                       }
#                       )
#     else:
#         print('konhkohnkohn')
#         return render(request,'upfile/showfeature.html')

#数据库版
def showfeature(request):
    #  读取分析文件
    features = Features.objects.all()
    return render(request,'upfile/showfeature.html',
                      {
                          'featurelists':features,
                      }
                      )
    if featurelists:
        print('yeyeyeyye')
        return render(request,'upfile/showfeature.html',
                      {
                          'featurelists':featurelists,
                      }
                      )
    else:
        print('konhkohnkohn')
        return render(request,'upfile/showfeature.html')
def search(request):
    searchlist = []
    if request.method=='POST':
        title = request.POST.get('select')
        content = request.POST.get('content')
        if content:
            if title=='src':
                for feature in featurelists:
                    if feature['src']==content:
                        searchlist.append(feature)
            elif title=='dst':
                for feature in featurelists:
                    if feature['dst']==content:
                        searchlist.append(feature)

            elif title=='port':
                for feature in featurelists:

                    if str(feature['srcport'])==content or str(feature['dstport'])==content:
                        searchlist.append(feature)
            return render(request,'upfile/showfeature.html',
                          {
                              'featurelists':searchlist,
                          }
                          )
        else:
            return render(request,'upfile/showfeature.html')

def cutsession(request):
    if sessionlist:
        return render(request,'upfile/cutsession.html',
                      {
                          'featurelists':sessionlist,
                      }
                      )
    if filedir:
        project_path = os.path.abspath(os.getcwd())+'/'
        cd_dir_file=os.path.join(project_path, 'USTC-TK2016-master')
        subprocess.call(["cd",  cd_dir_file, "&&", "powershell", "./1_Pcap2Session.ps1",filename[-1]], shell=True)#python的路径用/
        print("完成按会话所有层切割")
        path = 'USTC-TK2016-master/2_Session/session'
        dir_file = os.path.join(project_path, path)
        files = os.listdir(dir_file)

        for f in files:
            dic = {}
            fpath = os.path.join(dir_file, f)
            dic =getfeatures1(fpath)
            sessionlist.append(dic)

        del_list = os.listdir(dir_file)
        for f in del_list:
            file_path = os.path.join(dir_file, f)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return render(request,'upfile/cutsession.html',{
            'featurelists':sessionlist,
        })
    else:
        return render(request, "upfile/cutsession.html")
def searchsession(request):
    searchsessionlist = []
    if request.method=='POST':
        title = request.POST.get('select')
        content = request.POST.get('content')
        if content:
            if title=='addr':
                for feature in sessionlist:
                    if feature['src']==content or feature['dst']==content:
                        searchsessionlist.append(feature)
            elif title=='port':
                for feature in featurelists:
                    if str(feature['srcport'])==content or str(feature['dstport'])==content:
                        searchsessionlist.append(feature)
            return render(request,'upfile/cutsession.html',
                          {
                              'featurelists':searchsessionlist,
                          }
                          )
        else:
            return render(request,'upfile/cutsession.html')
def cutflow(request):
    if flowlist:
        return render(request, 'upfile/cutflow.html',
                      {
                          'featurelists': flowlist,
                      }
                      )
    if filedir:
        project_path = os.path.abspath(os.getcwd()) + '/'
        cd_dir_file = os.path.join(project_path, 'USTC-TK2016-master')
        subprocess.call(["cd", cd_dir_file, "&&", "powershell", "./flow1.ps1", filename[-1]],
                        shell=True)  # python的路径用/
        print("完成按流所有层切割")
        path = 'USTC-TK2016-master/2_Session/flow'
        dir_file = os.path.join(project_path, path)
        files = os.listdir(dir_file)
        for f in files:
            dic = {}
            fpath = os.path.join(dir_file, f)
            dic = getfeatures1(fpath)
            flowlist.append(dic)

        del_list = os.listdir(dir_file)
        for f in del_list:
            file_path = os.path.join(dir_file, f)
            if os.path.isfile(file_path):
                os.remove(file_path)

        return render(request, 'upfile/cutflow.html', {
            'featurelists': flowlist,
        })
    else:
        return render(request, "upfile/cutflow.html")
def searchflow(request):
    searchflowlist = []
    if request.method=='POST':
        title = request.POST.get('select')
        content = request.POST.get('content')
        if content:
            if title=='src':
                for feature in flowlist:
                    if feature['src']==content:
                        searchflowlist.append(feature)
            elif title=='dst':
                for feature in flowlist:
                    if feature['dst']==content:
                        searchflowlist.append(feature)

            elif title=='port':
                for feature in flowlist:

                    if str(feature['srcport'])==content or str(feature['dstport'])==content:
                        searchflowlist.append(feature)
            return render(request,'upfile/cutflow.html',
                          {
                              'featurelists':searchflowlist,
                          }
                          )
        else:
            return render(request,'upfile/cutflow.html')

#展示一个时间段内有多少数据 ???得到微秒级时间毫秒时间戳13位，秒时间戳10位
def bigdataArea(request):
    date = []
    data = []
    num = 0
    if featurelists:
        print("bukong")
    else:
        print("kongkongkonwoshikong")
    if featurelists:
        currdate = featurelists[0]['date']
        for feature in featurelists:
            if feature['date']<=currdate+0.0001:
                num += 1
            else:
                strtime = str(currdate)
                strlist = strtime.split('.')
                dateArray = time.localtime(atoi(strlist[0]))
                datetime = time.strftime("%Y/%m/%d %H:%M:%S", dateArray)
                lasttime = datetime + "." + strlist[1][0:6]#不加切割会数据出现格外的几位数
                date.append(lasttime)
                data.append(num)
                currdate += 0.0001
                num=0
        return render(request,'upfile/bigdataArea.html',
                      {
                          'date':date,
                          'data':data,
                      }
                      )
    else:
        return render(request,'upfile/bigdataArea.html',
                      )

def getcomposeflow(request):
    list = []
    srclist = []
    count = []
    comflow = []
    srcdict = {}
    if request.method=='POST':
        num = request.POST.get('num')
        i=0
        if featurelists:
            for feature in featurelists :
                if feature not in list:
                    if i<int(num):
                        dic = {}
                        n = featurelists.count(feature)
                        count.append(n)
                        list.append(feature)
                        srclist.append(feature['src']+"|"+feature['dst'])
                        dic['addr'] = feature['src']+"|"+feature['dst']
                        dic['num'] = n
                        comflow.append(dic)
                        i += 1
                    else:
                        break
            for k, v in zip(srclist, count):
                srcdict.update({k: v}, )
            return render(request,'upfile/composeflow.html',{
                'piedict':json.dumps(srcdict),
                'comflow':comflow,
            })

        return render(request, 'upfile/composeflow.html'
                      )
    return render(request, 'upfile/composeflow.html'
                  )
def getcomposesession(request):
    list = []
    srclist = []
    count = []
    comsession = []
    srcdict = {}
    if request.method == 'POST':
        num = request.POST.get('num')
        i = 0
        if featurelists:
            for feature in featurelists:
                n1 = n2 = 0
                if feature not in list:
                    n1 = featurelists.count(feature)
                    feature1 = feature
                    a = feature1['src']
                    feature1['src'] = feature['dst']
                    feature1['dst'] = a
                    if feature1 in featurelists:
                        n2 = featurelists.count(feature1)
                    if i < int(num):
                        dic = {}
                        count.append(n1+n2)
                        list.append(feature)
                        srclist.append(feature['src']+"|"+feature['dst'])
                        dic['addr'] = feature['src']+"|"+feature['dst']
                        dic['num'] = n1+n2
                        comsession.append(dic)
                        i += 1
                    else:
                        break
            for k, v in zip(srclist, count):
                srcdict.update({k: v}, )
            return render(request, 'upfile/composesession.html', {
                'piedict': json.dumps(srcdict),
                'comsession':comsession,
            })

        return render(request, 'upfile/composesession.html'
                      )
    return render(request, 'upfile/composesession.html'
                  )
#统计一个时间段内端口号的的使用情况
def portpie(request):

    srcport = []
    srcnum = []
    dstport = []
    dstnum = []
    port = []
    srcdict = {}
    dstdict = {}
    if featurelists:
        print("true")
        for feature in featurelists:
            #得到所有的端口号列表
            # if feature['srcport'] not in port:
            #     port.append(feature['srcport'])
            # if feature['dstport'] not in port:
            #     port.append(feature['dstport'])

            if feature['srcport'] not in srcport:
                srcport.append(feature['srcport'])
                n = srcport.index(feature['srcport'])
                srcnum.append(0)
                srcnum[n] = 1
            else:
                n = srcport.index(feature['srcport'])
                srcnum[n] += 1
            if feature['dstport'] not in dstport:
                dstport.append(feature['dstport'])
                n = dstport.index(feature['dstport'])
                dstnum.append(0)
                dstnum[n] = 1
            else:
                n = dstport.index(feature['dstport'])
                dstnum[n] = 1
        for k,v in zip(srcport,srcnum):
            srcdict.update({k:v},)
        for k,v in zip(dstport,dstnum):
            dstdict.update({k:v},)
        sort_s=sorted(srcdict.items(),key = lambda srcdict:srcdict[1],reverse=True)
        sort_d = sorted(dstdict.items(), key=lambda srcdict: srcdict[1], reverse=True)
        frontsrc = dict(sort_s[:10])
        frontdst = dict(sort_d[:10])
        frontport = list(frontsrc.keys())
        for key in frontdst.keys():
            if key not in frontport:
                frontport.append(key)
        return render(request,'upfile/portpie.html',
                      {
                          'srcport':json.dumps(frontsrc),
                          'dstport':json.dumps(frontdst),
                          'port':json.dumps(frontport),
                      }
                      )
    print("false")
    return render(request,'upfile/portpie.html')