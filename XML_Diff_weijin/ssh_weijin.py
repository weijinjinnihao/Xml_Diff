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


def getarray(ip, str2, username, password, port, path, localpath, destpath, name):
    downloadFile(ip, str2, username, password, port, localpath, name)
    parseToXML(path, destpath)
    return readXml(destpath)


def getname(ip, shell, username, password, port, n):
    n = execs(ip, "find / -name edits_inprogress_*", username, password, port)
    array = n.split("/")
    return n, array[len(array) - 1]


def get_str(ips, username, password, port):
    ips=[]
    n=[]
    name=[]
    path=[]
    destpath=["/home/a.xml","/home/b.xml","/home/c.xml"]

    for ip in ips:
        n,name = getname(ip,"find / -name edits_inprogress_*", username, password, port, n)

    for l in n:
        print(l)
    for i in (len(ips[])-1)：
        path[i]= "/home/path" + name[i]
        str[i]=getarray(ip[i],n[i],username, password, port, path1, "/home/a/", destpath1, name1)
    path1 = "/home/a/" + name1
    destpath1 = "/home/a.xml"
    path2 = "/home/b/" + name2
    destpath2 = "/home/b.xml"
    path3 = "/home/c/" + name3
    destpath3 = "/home/c.xml"
    str1 = getarray(ip1, n1, username, password, port, path1, "/home/a/", destpath1, name1)
    str2 = getarray(ip2, n2, username, password, port, path2, "/home/b/", destpath2, name2)
    str3 = getarray(ip3, n3, username, password, port, path3, "/home/c/", destpath3, name3)

# if __name__ == '__main__':
#     ip1 = '192.168.0.41'
#     ip2 = '192.168.0.42'
#     ip3 = '192.168.0.44'
#     username = 'root'
#     password = '111111'
#     port = 22
#     interval = 5
#     Get_File.run(interval,get3str(ip1,ip2,ip3, username, password, port))


