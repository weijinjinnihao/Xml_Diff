#!/usr/bin/env python
# coding: utf-8

# In[1]:


import xml.etree.ElementTree as ET
import numpy as np
import ssh

ignore_list = ['TIMESTAMP', 'MTIME', 'ATIME']

# line number
line_id = 0


# In[2]:


def walkData(root_node, result_list):
    global line_id
    line_id += 1
    root_tag = root_node.tag
    text = root_node.text
    # if(text==None):
    #     print(root_tag+' '+"Text is none...\n")
    if (root_tag not in ignore_list):
        temp_list = [root_tag, text, line_id]
        result_list.append(temp_list)

    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        walkData(child, result_list)
    return


# in:
#   a file
# out:
#   records_list: a list of records
#   record is a list of lines
def getXmlData(file_name):
    # level = 1 #节点的深度从1开始
    result_list = []
    root = ET.parse(file_name).getroot()
    # walkData(root, level, result_list)
    walk_data_by_records(root, result_list)
    return result_list


def walk_data_by_records(root_node, result_list):
    record_list = []
    root_tag = root_node.tag
    if (root_tag == 'RECORD'):
        # this is a records node
        # should return a list of this record

        # line id
        global line_id
        line_id = 0
        walkData(root_node, record_list)

        result_list.append(record_list)
    elif (root_tag == 'EDITS'):
        children_node = root_node.getchildren()

        if len(children_node) == 0:
            return
        for child in children_node:
            walk_data_by_records(child, result_list)
    else:
        pass


def str_xml_list(xml_list):
    """
    :param xml_list: a <list> like : ['OPCODE','OP_ADD']
    :return: a str like '   <OPCODE>OP_ADD'
    """
    tmp = '   '
    try:
        # for i in xml_list:
        #     if(i!=None):
        #         if(i!='\n'):
        #             tmp=tmp+i
        if (xml_list[0] != None):
            if (xml_list[1] != None):
                if (not xml_list[1].startswith('\n')):
                    tmp = '    <' + xml_list[0] + '>: ' + xml_list[1]
                else:
                    if (xml_list[0] == "DATA"):
                        tmp = ''
                    else:
                        tmp = '    <' + xml_list[0] + '>: '
            else:
                tmp = '    <' + xml_list[0] + '>: '
        return tmp
    except:
        if (xml_list[0] != None):
            if (xml_list[1] != None):
                if (not xml_list[1].startswith('\n')):
                    return xml_list[0] + xml_list[1]
                else:
                    return '    <' + xml_list[0] + '>: '
            else:
                return xml_list[0]
        else:
            return "【error】: List is NULL"


# In[3]:



# In[4]:


def get_last_block(file_list,op):
    Block=[]
    for i in range(len(file_list)):
        if (file_list[i][1][1]==op):
            for l in file_list[i]:
                if(l[0]=="BLOCK_ID"):
                    Block.append(l[1])
    return Block[-1]


# In[5]:


def get_op_list(file_list,op):
    op_list=[]
    for i in range(len(file_list)):
        if (file_list[i][1][1]==op):
            op_list.append(file_list[i])
    return op_list
test_list=getXmlData("NN41.xml")
op_test_list=get_op_list(test_list,"OP_ADD_BLOCK")

def get_block(op_list):
    path=[[[],""]]
    ret_block=[]
    ret=()
    for list in op_list:
        tmp_path=[]
        ret_block=[]
        for l in list:
            if(l[0]=="PATH"):
                for i in range(len(path)-1,-1,-1):
                    if(l[1]==path[i][1]):
                        path.append([path[i][0]+1,l[1]]) 
                        tmp_path.append([path[i][0]+1,l[1]])
                        break
                    else:
                        if (i==0):
                            path.append([1,l[1]])
                            tmp_path.append([1,l[1]])

        for l in list:
            if(l[0]=="BLOCK_ID"):
                ret_block.append(l[1])
        ret=np.append(ret,[tmp_path,ret_block])
    return ret
       


# print(ret)
# for r in ret:
#     print(r)
# np.savetxt("test.txt",ret,fmt="%r",delimiter=',')

# for r in ret:
#     r=np.array(r)
#     np.savetxt("test.txt",r,fmt="%r",delimiter=',')

if __name__ == '__main__':
    ip1 = '192.168.0.41'
    ip2 = '192.168.0.42'
    ip3 = '192.168.0.44'
    username = 'root'
    password = '111111'
    port = 22
    ssh.get3str(ip1,ip2,ip3, username, password, port)
    file1 = "/home/weijin/nn1_41.xml"
    file2 = "/home/weijin/nn2_42.xml"
    file3 = "/home/weijin/nn3_44.xml"

    file1_list=getXmlData(file1)
    file2_list=getXmlData(file2)
    file3_list=getXmlData(file3)
    last_block1=get_last_block(file1_list,"OP_ALLOCATE_BLOCK_ID")
    last_block2=get_last_block(file2_list,"OP_ALLOCATE_BLOCK_ID")
    last_block3=get_last_block(file3_list,"OP_ALLOCATE_BLOCK_ID")
    print([last_block1,last_block2,last_block3])

    op_test_list1=get_op_list(file1_list,"OP_ADD_BLOCK")
    ret1=get_block(op_test_list1)
    np.savetxt("nn1.txt",ret1,fmt="%r",delimiter=',')
    op_test_list2=get_op_list(file2_list,"OP_ADD_BLOCK")
    ret2=get_block(op_test_list2)
    np.savetxt("nn2.txt",ret2,fmt="%r",delimiter=',')
    op_test_list3=get_op_list(file3_list,"OP_ADD_BLOCK")
    ret3=get_block(op_test_list3)
    np.savetxt("nn3.txt",ret3,fmt="%r",delimiter=',')
    
    res=()
    for i in range(int(len(ret1)/2)):
        if((ret1[i*2]==ret2[i*2]) and (ret1[i*2+1]==ret2[i*2+1])):
            if((ret1[i*2]==ret3[i*2]) and (ret1[i*2+1]==ret3[i*2+1])):
                pass
            else:            
                res=np.append(res,[ret1[i*2],ret2[i*2],ret3[i*2]])
        else:
            res=np.append(res,[ret1[i*2],ret2[i*2],ret3[i*2]])
    # for l in res:
    #     print(l)


    if(len(res)==0):
        print("all the same!")
    else:
        np.savetxt("res_test1.txt",res,fmt="%r",delimiter=',')    
