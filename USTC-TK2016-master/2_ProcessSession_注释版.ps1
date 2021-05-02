# Wei Wang (ww8137@mail.ustc.edu.cn)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file, You
# can obtain one at http://mozilla.org/MPL/2.0/.
#执行第三步图像生成，将文件整理为784个字节
# ==============================================================================

$SESSIONS_COUNT_LIMIT_MIN = 0
$SESSIONS_COUNT_LIMIT_MAX = 60000
$TRIMED_FILE_LEN = 784
$SOURCE_SESSION_DIR = ".\2_Session\AllLayers"

echo "If Sessions more than $SESSIONS_COUNT_LIMIT_MAX we only select the largest $SESSIONS_COUNT_LIMIT_MAX."
echo "Finally Selected Sessions:"

$dirs = gci $SOURCE_SESSION_DIR -Directory
#遍历2-session\L7下的文件夹：BitTorrent-L7
foreach($d in $dirs)
{
#BitTorrent-L7下的文件
    $files = gci $d.FullName
#BitTorrent-L7下的文件的数量
    $count = $files.count

# 如果数量满足大于最小量$d.Name=BitTorrent-L7
    if($count -gt $SESSIONS_COUNT_LIMIT_MIN)
    {      
        echo "Finally Selected Sessions:"
        echo("1111111111")       
        echo "$($d.Name) $count"  
       #如果数量超过最大量      
        if($count -gt $SESSIONS_COUNT_LIMIT_MAX)
        {
	#将文件大小从大到小排序选择前max个
            $files = $files | sort Length -Descending | select -First $SESSIONS_COUNT_LIMIT_MAX
            $count = $SESSIONS_COUNT_LIMIT_MAX
        }
#解析路径中的通配符，显示文件的路径
        $files = $files | resolve-path
#随机选择count/10个文件
        $test  = $files | get-random -count ([int]($count/10))
#该文件是否包含在BitTorrent-L7中
        $train = $files | ?{$_ -notin $test}     

        $path_test  = "3_ProcessedSession\FilteredSession\Test\$($d.Name)"
        $path_train = "3_ProcessedSession\FilteredSession\Train\$($d.Name)"
#创建目录
        ni -Path $path_test -ItemType Directory -Force
        ni -Path $path_train -ItemType Directory -Force    
#将$test(包括文件路径和文件名）中选中的文件移动到$path_test
        cp $test -destination $path_test        
        cp $train -destination $path_train
    }
}


#将所有文件分割为大小784
echo "All files will be trimed to $TRIMED_FILE_LEN length and if it's even shorter we'll fill the end with 0x00..."
#创建一个数组
$paths = @(('3_ProcessedSession\FilteredSession\Train', '3_ProcessedSession\TrimedSession\Train'), ('3_ProcessedSession\FilteredSession\Test', '3_ProcessedSession\TrimedSession\Test'))
foreach($p in $paths)
{
    foreach ($d in gci $p[0] -Directory) 
    {
#创建3_ProcessedSession\TrimedSession\Train\BitTorrent-L7目录

        ni -Path "$($p[1])\$($d.Name)" -ItemType Directory -Force
        foreach($f in gci $d.fullname)
        {
#按字节读取文件内容
            $content = [System.IO.File]::ReadAllBytes($f.FullName)
#文件长度大于784,截断
            $len = $f.length - $TRIMED_FILE_LEN
            if($len -gt 0)
            {        
                $content = $content[0..($TRIMED_FILE_LEN-1)]        
            }
#文件长度小于784,补全
            elseif($len -lt 0)
            {        
                $padding = [Byte[]] (,0x00 * ([math]::abs($len)))
                $content = $content += $padding
            }
#在文件BitTorrent-L7目录的挨个文件里指定编码覆盖写入内容$content
            Set-Content -value $content -encoding byte -path "$($p[1])\$($d.Name)\$($f.Name)"
        }        
    }
}