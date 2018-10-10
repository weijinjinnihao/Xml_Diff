import xml.etree.ElementTree as ET

file1='b.xml'
file2='b.xml'

#-*- coding: UTF-8 -*- 
# 从文件中读取数据
import xml.etree.ElementTree as ET
 
#全局唯一标识
unique_id = 1

# txid list
# txid_list=list()

#遍历所有的节点
def walkData(root_node, level, result_list):
    global unique_id    # solve error: using before assignment

    root_tag = root_node.tag
    text=root_node.text
    # if(text==None):
    #     print(root_tag+' '+"Text is none...\n")
    if(root_tag!='TIMESTAMP'):
        temp_list =[unique_id, level, root_tag, text]
        result_list.append(temp_list)

    unique_id += 1
    
    #遍历每个子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        walkData(child, level + 1, result_list)
    return
 
#out:
#[
#    #ID, Level, Attr Map
#    [1, 1, {'ID':1, 'Name':'test1'}],
#    [2, 1, {'ID':1, 'Name':'test2'}],
#]
def getXmlData(file_name):
    level = 1 #节点的深度从1开始
    result_list = []
    root = ET.parse(file_name).getroot()
    walkData(root, level, result_list)
 
    return result_list

# compare two list on given rules
# out:
#   a list
#   output only if different
#   output a list containing the difference info
def compare_list(list1,list2,diff_position):
    output=list()
    # l1=len(list1)
    # l2=len(list2)
    # try:
    #     assert(l1==l2)
    # except:
    #     print("the length of two input list is not equal")
    # try:
    #     assert(diff_position<=l1)
    # except:
    #     print("diff_position exceeds the length")
    #
    # try:
    #     assert(list1[1]==list2[1])
    # except:
    #     print("The two comparing list is not the at the same position")
    try:
        if(list1[diff_position]!=list2[diff_position]):
            tmp=list1[diff_position]+" -- "+list2[diff_position]
            output=list1
            output[diff_position]=tmp

        else:
            output=list()
        return output
    except:
        print(list1)
        print(list2)
def write_file(diff_list,xml_list):
    fp=open("output",'w+')
    for l in diff_list:
        txid = get_txid_on_line_number(l,xml_list)
        if(txid==0):
            fp.write('******** OOOPS! TXID NOT FOUND ********* \n')
        else:
            fp.write('TXID = '+str(txid)+'\n')
        num_tabs=int(l[1])
        tabs=''
        for i in range(num_tabs-1):
            tabs+='  '
        fp.write(tabs+l[2]+' '+l[3]+'\n')
    fp.close()
# ret:
    # a integer
    # the txid
    # =0 if not found
def get_txid_on_line_number(line,xml_list):
    keyword=line[2]
    ret=0
    list_len=len(xml_list)
    ind=int(line[0])
    if(keyword=='OPCODE'):
        while(ind<=list_len-1):
            crnt_list=xml_list[ind]
            if(crnt_list[2]!='TXID'):
                ind=ind+1
            else:
                ret=int(crnt_list[3])
                break
    else:
        while(ind>=0):
            crnt_list=xml_list[ind]
            if(crnt_list[2]!='TXID'):
                ind=ind-1
            else:
                ret=int(crnt_list[3])
                break

    return ret


if __name__=='__main__':
    file1_list=getXmlData(file1)
    unique_id = 1
    file2_list=getXmlData(file2)

    result=list()

    len1=len(file1_list)
    len2=len(file2_list)

    len_min=min({len1,len2})

    for i in range(0,len_min):
        # for each list
        list1=file1_list[i]
        list2=file2_list[i]

        comp_rslt=compare_list(list1,list2,3)
        if (len(comp_rslt)!=0):
            result.append(comp_rslt)
    write_file(result,file1_list)
    

