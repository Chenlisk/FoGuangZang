#--------------------------------------------------------------------------------------
import datetime
import os
import re
import sys
import time

# -------------------------------------------------------------------------------------------
Path = 'foguang'
Path = 'foguang\\阿含藏'
# -------------------------------------------------------------------------------------------
def main(base=0, lens=1):
    fileList = []
    for dirpath, dirnames, filenames in os.walk(Path):
        for file in filenames:
            if file.endswith('.htm'):
                fileList.append(os.path.join(dirpath, file))

    top = base + lens

    if -1 == lens:
        top = len(fileList)

    for i in range(base, top, 1):
        data = readFile(fileList[i])
        process(data, fileList[i])
        tim = str(datetime.datetime.now())[0:-7]
        print(tim, ' ---> ','\a', str(i + 1).rjust(3, '0'), '/', len(fileList), '---$:', fileList[i])


# ==========================================================
def process(data, path):
    f = path[path.find('\\') + 1:]
    f = f[:f.rfind('\\')][f.find('\\'):]
    path1 = path.replace(f, '').replace('foguang', 'Result')

    path2 = path.replace('foguang', 'Result2')

    data = preProcess(data)
    # addr = path1.replace('.htm', '.txt')  
    addr = path2.replace('.htm', '.out')  


    
    if data != None:
        writeFile(addr, data)

        # if data.find('<')!=-1:
        #     print(data[data.find('<'):data.find('<')+10],path)
        #     sys.exit(0)


def preProcess(data):
    data=data.lower()

    check = re.search(r"<td width='100%'(.|\n)+?注解(.|\n)+?</td>", data)
    if check != None:
        return None
    check = re.search(r"<td width='100%'(.|\n)+?注釋(.|\n)+?</td>", data)
    if check != None:
        return None    
    check = re.search(r"<td width='100%'(.|\n)+?題解(.|\n)+?</td>", data)
    if check != None:
        return None    
    check = re.search(r"<td width='100%'(.|\n)+?凡例(.|\n)+?</td>", data)
    if check != None:
        return None    
    if re.search(r"<center>", data) == None:
        return None    
    if re.search(r"<table border='0' width='85%'>", data) == None and re.search(r'<table border="0" width="85%">', data) == None:
        return None    
    
    data = re.sub(r'\n', '', data)

    pattern = re.compile(r'<span style="font-size: 10pt;">.+?</span>')  # 查找数字
    s = pattern.findall(data)
    for i in range(len(s)):
        pstr = s[i]
        pstr = pstr.replace('<span style="font-size: 10pt;">', '（').replace('</span>', '）')
        data = data.replace(s[i], pstr)

    w = re.findall(r'&#\d{3,5};', data)
    for i in range(len(w)):
        h = hex(int(w[i][2:-1]))
        h = chr(eval(h))
        data = data.replace(w[i], h)

    # head = r"<font size='3' face='新細明體'.+?<p (align='left' )?style='line-height: 150%'>"
    head = r"<p (align='left' )?style=[\'\"]line-height: 150%[\'\"]>"
    data = re.sub(head,'#@@@#',data)
    head = '#@@@#'
    data = data[data.find(head):]
    data = data.replace(head,'<p>')
    
    data = re.sub(r"<table border='1' width='85%'>(.|\n)+?</table>", '', data)    
    data = re.sub(r'<table border="1" width="85%">(.|\n)+?</table>', '', data)    
    data = re.sub(r'<table width="85%" border=1>(.|\n)+?</table>', '', data)   
    data = re.sub(r"<table width='85%' border=1>(.|\n)+?</table>", '', data) 

    data = re.sub(r'\(.{0,}?<a.+?\)</a>', '', data)
    data = re.sub(r'<a.+?</a>', '', data)
    data = re.sub(r'\x09', '', data)
    data = re.sub(r'\[p\d{1,4}\]', '', data)
    data = re.sub(r'p\d{1,4}', '', data)    
    data = re.sub(r'<span (style|lang).+?>','',data)
    data = re.sub(r'<font.+?>','<p>',data)   
    data = re.sub(r'<sup.+?</sup>','',data)   
    data = re.sub(r'(　| |&nbsp;|</?b>|</?i>|<hr>|</?pre>|</span>|</?strong>|</font>|<GC>|<GCFSM@17>|<GCFMM@17>|<GEMME@12>|<bt1,0,2>|<em>|<bx>|<d0>|<sub>|<i2>|<st1:chmetcnv.+?>|<font face.+?size.+?>|<div align.+?>|<center>|<pre.+?>)','',data,0,re.I)
    data = re.sub(r'(<br/?>|<tr>|<td>|<pstyle.+?>)', '<p>', data)  
    
    data = re.sub(r'）+', '）', data)
    data = re.sub(r'（+', '（', data)
    data = re.sub(r'</.+?>', '', data)
    data = re.sub(r'<[a-z]{3}.+?>', '', data)
    data = re.sub(r'(<p>)+', '<p>', data)
    data = re.sub(r'<p>，', '，', data)
    data = re.sub(r'<p>。', '。', data)
    if data.endswith('<p>'):
        data=data[0:-3]

    # data = re.sub(r'<p>', '\n', data)


    return data


def readFile(filedir):
    with open(filedir, "r", encoding='utf-8') as f:
        string = f.read()
    return string


def writeFile(filedir, string):
    if filedir.find('\\') != -1:
        path = filedir[0:filedir.rfind("\\")]
        if not os.path.exists(path):
            os.makedirs(path)
    with open(filedir, "w+", encoding='utf-8') as f:
        f.write(string)


# ==========================================================
if __name__ == '__main__':
    x = 1
    y = 1
    if len(sys.argv) > 2:
        y = sys.argv[2]
        y = int(y)
        x = sys.argv[1]
        x = int(x) - 1
        main(x, y)
    elif len(sys.argv) > 1:
        x = sys.argv[1]
        x = int(x) - 1
        main(x, y)
    else:
        main()
    # ==========================================================
