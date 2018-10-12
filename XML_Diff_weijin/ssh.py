import paramiko
import time, threading
import re,os
import os.path
import xml.etree.ElementTree as ET

def getTagvalue (xmlpath ,tagname ):
    array=[]
    tree = ET.ElementTree(file=xmlpath)
    for elem in tree.iter(tag=tagname):
        array.append(str(elem.text))
    return array

def execs(ip, cmd, username, password,port):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, port, username, password)
    stdin, stdout, stderr = s.exec_command(cmd)
    str1=str(stdout.read())
    s.close()
    return str1[2:-3]

def writefile(filepath,content):
    f = open(filepath, 'w')
    f.write(content)
    f.close()

def readXml(xmlpath):
    f = open(xmlpath, 'r')
    array=f.readlines();
    return array

def parseToXML(path,dstpath):
    os.system("hdfs oev -i "+path+" -o "+ dstpath)

def downloadFile(ip,srcpath,username,password,port,localpath,name):
    scp = paramiko.Transport((ip,port))
    scp.connect(username=username,password=password)
    sftp=paramiko.SFTPClient.from_transport(scp)
    sftp.get(srcpath,os.path.join(localpath,name))
    scp.close()

def getarray(ip, str2,username,password, port,path,localpath ,destpath,name):
    downloadFile(ip, str2,username, password, port, localpath,name)
    parseToXML(path, destpath)
    return readXml(destpath)

def getname(ip,shell,username,password,port,n):
    n = execs(ip, "find / -name edits_inprogress_*", username, password, port)
    array = n.split("/")
    return n,array[len(array) - 1]

def get3str(ip1,ip2,ip3, username, password, port):
    n1=""
    n2=""
    n3=""
    n1,name1=getname(ip1,"find / -name edits_inprogress_*", username, password, port,n1)
    n2,name2=getname(ip2,"find / -name edits_inprogress_*", username, password, port,n2)
    n3,name3=getname(ip3, "find / -name edits_inprogress_*", username, password, port,n3)
    # print(n1)
    # print(n2)
    # print(n3)
    # print(name1)
    path1 ="/home/weijin/nn1_41/"+name1
    destpath1 = "/home/weijin/nn1_41.xml"
    path2="/home/weijin/nn2_42/"+name2
    destpath2 = "/home/weijin/nn2_42.xml"
    path3="/home/weijin/nn3_44/"+name3
    destpath3 = "/home/weijin/nn3_44.xml"
    str1 = getarray(ip1, n1, username, password, port, path1, "/home/weijin/nn1_41/",destpath1,name1)
    str2 = getarray(ip2, n2,username, password, port, path2, "/home/weijin/nn2_42/",destpath2,name2)
    str3 = getarray(ip3, n3,username, password, port, path3, "/home/weijin/nn3_44/",destpath3,name3)
    


# if __name__ == '__main__':
#     ip1 = '192.168.0.41'
#     ip2 = '192.168.0.42'
#     ip3 = '192.168.0.44'
#     username = 'root'
#     password = '111111'
#     port = 22
#     interval = 5
#     Get_File.run(interval,get3str(ip1,ip2,ip3, username, password, port))


