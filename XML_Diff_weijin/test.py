import xml.etree.ElementTree as ET
import time
import ssh

# sorry for using global
# since it is easier to add this feature
ignore_list = ['TIMESTAMP', 'MTIME', 'ATIME']

# line number
line_id = 0


# txid list
# txid_list=list()

# for each node of root
# append the line to list
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


def compare_list_diff(list1,list2,diff_position,txid,ret_list):
    """
    compare two list on given rules
    out:
        append a list to ret_list which will be written into files
        output only if different
        output a list containing the difference info
    """
    output=list()

    try:
        if(list1[diff_position]!=list2[diff_position]):
            # wtite txid only once for each record
            if(len(ret_list)==0):
                ret_list.append(txid)
                ret_list.append("The Diff Part:\n")
            else:
                pass
            tmp=' (NN41)  '+list1[diff_position]+" -- "+'(NN42)'+list2[diff_position]
            head='  ('+'Line Number: '+str(list1[2])+')'+'<'+list1[0]+'>'
            output=head+tmp
        else:
            pass

        if(len(output)!=0):
            ret_list.append(output)
    except:
        print(" From compare_list Except......")
        print('<TXID>' + str(txid))
        print(list1)
        print(list2)

def operate_TXID(file_list,op):
    operate_TXID=[]
    for i in range(len(file_list)):
        if (file_list[i][1][1]==op):
            operate_TXID.append(i+1)
    return operate_TXID

def list_ALL_MK(txid,list,op):
    ret=[]
    ret.append([txid,op])
    for l in list:
        if ((l[0]=="BLOCK_ID") or (l[0]=="INODEID")):
            ret.append(l)
    for l in list:
        if (l[0] == "PATH"):
            ret.append(l)
    return ret

def get_BLOCK_INODE(list,op):
    ret=[]
    txid=operate_TXID(list,op)
    for t in txid:
        ret.append(list_ALL_MK(t,list[t-1],op))
    return ret





if __name__ == '__main__':

    file1_list=[]
    file2_list=[]
    file3_list=[]
    file1_list = getXmlData("NN41.xml")
    file2_list = getXmlData("NN42.xml")
    file3_list = getXmlData("NN44.xml")


    list1=get_BLOCK_INODE(file1_list,"OP_ADD")
    list2=get_BLOCK_INODE(file2_list,"OP_ADD")
    list3=get_BLOCK_INODE(file3_list,"OP_ADD")
    print(list1)
    print("\n")
    print(list2)
    print("\n")
    print(list3)

    # res=com_ALL_MK(list1,list2,list3)
    # print(res)
    # print(a)
    # print("\n")
    # print(b)
    #
    # block_1=get_BLOCK(t1, file1_list,"OP_ALLOCATE_BLOCK_ID")
    # block_2 = get_BLOCK(t2, file2_list, "OP_ALLOCATE_BLOCK_ID")
    # block_3 = get_BLOCK(t3, file3_list, "OP_ALLOCATE_BLOCK_ID")
    # print(block_1)
    # print(block_2)
    # print(block_3)
    # result=compare_files_by_allocate_mkdir("allocate","blockid",block_1, block_2,block_3)
    # print(result)
    #
    # # print(result)

