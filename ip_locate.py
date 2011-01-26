# -*- coding: utf-8 -*-
# encoding: utf-8

import os,sys
import re
from urllib2 import build_opener
import BeautifulSoup
from BeautifulSoup import BeautifulSoup
from progressBar import *

VERSION="1.2"

ip_or_file = sys.argv[1]
output_dict = {}
output_file = "ip_locate_info_tmpk.txt"
#不能匹配的ip
err_output_file = "err_ip_address.txt"
dict_file_txt = open("nodist_city.txt")
dict_file = dict_file_txt.readlines()
lineno = 0

def get_correct_fommat(info,ip_address):
    for i in dict_file:
        data = i.split('|')
        if data[1] in info:
            il = data[:4]
            full_info = "%s|%s|%s|%s|%s" %(ip_address,il[3],il[2],il[0],il[1])
        # elif data[0] in info:
        #     il = data[:4]  
        #     full_info = "%s|%s|%s|%s|%s" %(ip_address,il[3],il[2],il[0],il[1])  
    return full_info
# get prov/city info from dict
def get_correct_formmat_province(info,ip_address):
    for i in dict_file:
        if info in i:
            data = i.split('|')[:4]
            if info in data and data[2]==data[3]:
                new_full = "%s|%s|%s|%s|%s" %(ip_address,data[3],data[2],data[0],data[1])
    return new_full            
def get_location_info_from_nodist(address_string,ip_address):
    b = str(address_string).strip().split("：")[1].split(" ")[0]
    p = b.strip()
    try:
        try:
            x_info = get_correct_fommat(p,ip_address)
        except:
            x_info = get_correct_formmat_province(p,ip_address)
    except:
        pass
    return x_info

def get_ip_locate(ip_address):
    errf = open(err_output_file,'a')
    opener = build_opener()
    result_info = ''
    avaliable_list = []
    err_list = []
    result_list = []
    url = 'http://www.ip138.com/ips.asp?ip=%s&action=2' %ip_address
    page = opener.open(url).read()
    soup = BeautifulSoup(page)
    a = soup.findAll('table')[2].findAll("tr")[2].findAll('li')
    for i in a:
        k = i.string
        try:
            j = get_location_info_from_nodist(k,ip_address)
            result_list.append(j)
        except:
            err_address = "%s|%s"%(k,ip_address)
            errf.write("%s\n"%err_address.encode('utf-8'))
    if '省' in  result_list[0] or '市' in result_list[0] or '区' in result_list[0]:                
        result_info = result_list[0]
    elif '省' not in  result_list[0] or '市' not in result_list[0]:
        for i in result_list:
            if '省' in i or '市' in i:
                avaliable_list.append(i)
                result_info = avaliable_list[0]
    return result_info

# Regular Expression for is a IP Address or not
p=r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])'

ip_list = re.findall(p,ip_or_file)

if ip_list != []:
    outf = open(output_file,'a')
    errf = open(err_output_file,'a')
    try:
        outf.write("%s\n" %(get_ip_locate(ip_or_file)))
        print u'已输出到文本:',output_file
    except:
        # errf.write("%s\n" %(str(ip_or_file)))
        # errf.flush()
        print u'没有匹配的IP,已输出到err日志:',err_output_file
        pass        
    outf.close()
    errf.close()
else :
    #如果文件名字不包含全路径，则默认为当前目录
    if os.sep not in ip_or_file:
        ip_or_file = os.getcwd()+os.sep+ip_or_file
    if not os.path.exists(ip_or_file):
        print u'您输入的文件文件名称有误'
        usage()
        sys.exit(1)
    try:
        filename = open(ip_or_file)
        outf = open(output_file,'a')
        errf = open(err_output_file,'a')
        file_line = open(ip_or_file).readlines()
        flie_line_no = file_line.__len__()
        prog = progressBar(0,flie_line_no,75)
        for i in filename.readlines():
            i = i.strip()
            lineno += 1
            try:
                locate_info = get_ip_locate(str(i))
                output_dict[str(i)]=locate_info
                outf.write("%s\n"%locate_info)
                outf.flush()
                print prog(lineno),
            except:
                # errf.write("%s\n" %(str(i)))
                # errf.flush()
                pass
        outf.close()
        # errf.close()
        sys.exit(0)
    except:
        outf = open(output_file,'a')
        print u'未找到文件'
        sys.exit(0)
    outf.close() 
    errf.close()   
