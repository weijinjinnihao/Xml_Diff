import paramiko
import time, threading
import re, os
import os.path
import xml.etree.ElementTree as ET


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


def parseToXML(path, dstpath):
    os.system("hdfs oev -i " + path + " -o " + dstpath)


def downloadFile(ip, srcpath, username, password, port, localpath, name):
    scp = paramiko.Transport((ip, port))
    scp.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(scp)
    sftp.get(srcpath, os.path.join(localpath, name))
    scp.close()


def getarray(ip, string, username, password, port, path, localpath, destpath, name):
    downloadFile(ip, string, username, password, port, localpath, name)
    parseToXML(path, destpath)
    return readXml(destpath)


def getname(ip, shell, username, password, port):
    n = execs(ip, "find / -name edits_inprogress_*", username, password, port)
    return n

def get_str(ip, username, password, port):
    n=[]
    name=[]
    path=[]
    string=[]
    destpath=["/home/a.xml","/home/b.xml","/home/c.xml"]
    for i in range(len(ip)):
        n.append(getname(ip[i],"find / -name edits_inprogress_*", username, password, port))
    for l in (n):
        array=l.split("/")
        name.append(array[len(array) - 1])
    for i in range(len(n)):
        path.append("/home/path" + name[i])
        string.append(getarray(ip[i], n[i], username, password, port, path[i], "/home/a/", destpath[i], name[i]))
    for l in n:
        print(l)

#     path1 = "/home/a/" + name1
#     destpath1 = "/home/a.xml"
#     path2 = "/home/b/" + name2
#     destpath2 = "/home/b.xml"
#     path3 = "/home/c/" + name3
#     destpath3 = "/home/c.xml"
#     str1 = getarray(ip1, n1, username, password, port, path1, "/home/a/", destpath1, name1)
#     str2 = getarray(ip2, n2, username, password, port, path2, "/home/b/", destpath2, name2)
#     str3 = getarray(ip3, n3, username, password, port, path3, "/home/c/", destpath3, name3)

if __name__ == '__main__':
    ip1 = '192.168.0.41'
    ip2 = '192.168.0.42'
    ip3 = '192.168.0.44'


    username = 'root'
    password = '111111'
    port = 22
    ip=[]
    get_ip=input("Which ip?:")
    get_ip =get_ip.split(",")
    print(len(get_ip))
    for l in get_ip:
        if (l=="ip1"):
            ip.append(ip1)
        if (l=="ip2"):
            ip.append(ip2)
        if (l=="ip3"):
            ip.append(ip3)
    for i in range(len(ip)):
        print(ip[i])

    # path=[]
    # destpath = ["/home/a.xml", "/home/b.xml", "/home/c.xml"]
    #
    # for i in range(len(ip)):
    #     path.append("/home/path")
    #     # str[i] = getarray(ip[i], n[i], username, password, port, path[i], "/home/a/", destpath[i], name[i])
    # for l in path:
    #     print(l)
    get_str(ip, username, password, port)


