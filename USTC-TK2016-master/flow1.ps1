# Wei Wang (ww8137@mail.ustc.edu.cn)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file, You
# can obtain one at http://mozilla.org/MPL/2.0/.
#流量分割 按流切割
# foreach循环遍历，gci是可以查看某个目录下的文件

# ==============================================================================

foreach($f in gci 1_Pcap *.pcap)   
{
if ($f.name -eq $args)
    {
        ## 0_Tool\SplitCap_2-1\SplitCap -p 50000 -b 50000 -r $f.FullName -o 2_Session\AllLayers\$($f.BaseName)-ALL
        ##读取文件，设置保留内存中的并行会话行数5000，缓冲的字节数5000，基于会话将pcap处理内容输出到2_Session\AllLayers,,,$($f.BaseName)-ALL??
    0_Tool\SplitCap_2-1\SplitCap -p 50000 -b 50000 -r $f.FullName -s flow -o 2_Session\flow

    gci 2_Session\flow | ?{$_.Length -eq 0} | del
    }
    else
    {
    continue;
    }
        # 如果当前处理文件的长度为0，则删除该文件

        # 0_Tool\SplitCap_2-1\SplitCap -p 50000 -b 50000 -r $f.FullName -o 2_Session\L7\$($f.BaseName)-L7 -y L7
        #0_Tool\SplitCap_2-1\SplitCap -p 50000 -b 50000 -r $f.FullName -s flow -o 2_Session\L7\$($f.BaseName)-L7 -y L7
        #gci 2_Session\L7\$($f.BaseName)-L7 | ?{$_.Length -eq 0} | del
}
0_Tool\finddupe -del 2_Session\flow
#？？？
#0_Tool\finddupe -del 2_Session\L7