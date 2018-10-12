import paramiko
import time, threading
import re, os
import os.path
import xml.etree.ElementTree as ET
import time

# get .xml file
def getTagvalue(xmlpath, tagname):
    array = []
    tree = ET.ElementTree(file=xmlpath)
    for elem in tree.iter(tag=tagname):
        array.append(str(elem.text))
    return array


def execs(ip, cmd, username, password, port):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, port, username, password)
    stdin, stdout, stderr = s.exec_command(cmd)
    str1 = str(stdout.read())
    s.close()
    return str1[2:-3]


def writefile(filepath, content):
    f = open(filepath, 'w')
    f.write(content)
    f.close()


def readXml(xmlpath):
    f = open(xmlpath, 'r')
    array = f.readlines();
    return array


# parse local_log_file in localpath to .xml, put them in xml_path
def parseToXML(local_log_file, xml_path):
    os.system("hdfs oev -i " + local_log_file + " -o " + xml_path)


# download log to localpath
def downloadFile(ip, srcpath, username, password, port, localpath, name):
    scp = paramiko.Transport((ip, port))
    scp.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(scp)
    sftp.get(srcpath, os.path.join(localpath, name))
    scp.close()


def getarray(ip, string, username, password, port, local_log_file, localpath, xml_path, name):
    downloadFile(ip, string, username, password, port, localpath, name)
    parseToXML(local_log_file, xml_path)
    return readXml(xml_path)


def getname(ip, shell, username, password, port):
    n = execs(ip, "find / -name edits_inprogress_*", username, password, port)
    return n

def get_str(ip, username, password, port):
    n=[]
    name=[]
    local_log_file=[]
    string=[]
    xml_path=["/home/weijin_1/nn1_41.xml","/home/weijin_1/nn2_42.xml","/home/weijin_1/nn3_44.xml"]
    localpath=["/home/weijin_1/nn1_41/","/home/weijin_1/nn2_42/","/home/weijin_1/nn3_44/"]
    for i in range(len(ip)):
        n.append(getname(ip[i],"find / -name edits_inprogress_*", username, password, port))
    for l in (n):
        array=l.split("/")
        name.append(array[len(array) - 1])
    for i in range(len(n)):
        local_log_file.append(localpath[i] + name[i])
        string.append(getarray(ip[i], n[i], username, password, port, local_log_file[i], localpath[i], xml_path[i], name[i]))
    # for l in n:
    #     print(l)

#     local_log_file1 = "/home/a/" + name1
#     xml_path1 = "/home/a.xml"
#     local_log_file2 = "/home/b/" + name2
#     xml_path2 = "/home/b.xml"
#     local_log_file3 = "/home/c/" + name3
#     xml_path3 = "/home/c.xml"
#     str1 = getarray(ip1, n1, username, password, port, local_log_file1, "/home/weijin_1/nn1_41/", xml_path1, name1)
#     str2 = getarray(ip2, n2, username, password, port, local_log_file2, "/home/weijin_1/nn2_42/", xml_path2, name2)
#     str3 = getarray(ip3, n3, username, password, port, local_log_file3, "/home/weijin_1/nn3_44/", xml_path3, name3)

# if __name__ == '__main__':
#     ip1 = '192.168.0.41'
#     ip2 = '192.168.0.42'
#     ip3 = '192.168.0.44'
#     username = 'root'
#     password = '111111'
#     port = 22
#     ip=[]
#     get_ip=input("Which ip?:[ip1/ip2/ip3?]")
#     get_ip =get_ip.split(",")
#     print(len(get_ip))
#     for l in get_ip:
#         if (l=="ip1"):
#             ip.append(ip1)
#         if (l=="ip2"):
#             ip.append(ip2)
#         if (l=="ip3"):
#             ip.append(ip3)
#     for i in range(len(ip)):
#         print(ip[i])


#   get_str(ip, username, password, port)


