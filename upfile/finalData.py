{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "#from PIL import Image\n",
    "import binascii\n",
    "import errno    \n",
    "import os\n",
    "def getArrayfrom_pcap(filename):#####把切割好的pacp文件转换成矩阵，8位一个整数保存\n",
    "    with open(filename, 'rb') as f:##以二进制形式打开filename'文件\n",
    "        content = f.read()##打开是16进制\n",
    "    hexst = binascii.hexlify(content)  #通过这个转化成16进制一维数组\n",
    "    fh = np.array([int(hexst[i:i+2],16) for i in range(0, len(hexst), 2)])  \n",
    "    #然后通过将2个16进制的数字合并，组成一个不超过256的10进制，依旧是一维数组\n",
    "    #到这一步我已经找到我需要的数据形式了，后面只是保存形式的不同而已 \n",
    "    return fh\n",
    "def mkdir_p(path):\n",
    "    try:\n",
    "        os.makedirs(path)#在给定的path目录下创建目录，\n",
    "        #os.makedirs('Desktop/toolkit/USTC-TK2016-master/3_ProcessedSession/TrimedSession/Train/test')这才是正确的语法\n",
    "    except OSError as exc:  # Python >2.5\n",
    "        if exc.errno == errno.EEXIST and os.path.isdir(path):\n",
    "            pass\n",
    "        else:\n",
    "            raise\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "path = 'C:/Users/dell/Desktop/Malware/'\n",
    "count = 0\n",
    "final = np.zeros((1,784))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "write+1\n",
      "write+1\n",
      "write end\n"
     ]
    }
   ],
   "source": [
    "with open('C:/Users/dell/Desktop/test-malware.txt', 'ab') as f:##支持连续写入不覆盖\n",
    "    for i,d in enumerate(os.listdir(path)):\n",
    "        p = os.path.join(path,d)\n",
    "        arr = getArrayfrom_pcap(p)###得到一维数组\n",
    "        arr = np.expand_dims(arr, axis = 0)###变成二维，不然无法append\n",
    "        count = count + 1\n",
    "        final = np.append(final,arr,axis=0)\n",
    "        ####final够五百就写入，然后清空\n",
    "        if(count == 500):\n",
    "            final = np.delete(final, 0, 0)\n",
    "            np.savetxt(f,final)#将array写入txt文件\n",
    "            final = np.zeros((1,784))#用0补充，清空\n",
    "            count = 0\n",
    "            print(\"write+1\")\n",
    "        else:\n",
    "            continue\n",
    "    if(count == 0):\n",
    "        pass\n",
    "    else:       #最后一点没有500个的时候\n",
    "        final = np.delete(final,0,0)\n",
    "        np.savetxt(f,final)\n",
    "        print(\"write end\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}