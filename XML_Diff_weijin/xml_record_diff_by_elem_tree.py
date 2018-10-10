
#-*- coding: UTF-8 -*- 

import xml.etree.ElementTree as ET


# sorry for using global
# since it is easier to add this feature
ignore_list = ['TIMESTAMP', 'MTIME', 'ATIME']


# txid   list
# txid_list=list()

# for each node of root
# append the line to list
def walkData(root_node, result_list):

    root_tag = root_node.tag
    text=root_node.text
    # if(text==None):
    #     print(root_tag+' '+"Text is none...\n")
    if(root_tag not in ignore_list):
        temp_list =[root_tag, text]
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
    walk_data_by_records(root,result_list)
    return result_list


def walk_data_by_records(root_node, result_list):
    record_list=[]
    root_tag = root_node.tag
    if(root_tag=='RECORD'):
        # this is a records node
        # should return a list of this record

        # line id
        line_id=0
        walkData(root_node,record_list)

        result_list.append(record_list)
    elif(root_tag=='EDITS'):
        children_node = root_node.getchildren()

        if len(children_node) == 0:
            return
        for child in children_node:
            walk_data_by_records(child,result_list)
    else:
        pass


def str_xml_list(xml_list):
    """
    :param xml_list: a <list> like : ['OPCODE','OP_ADD']
    :return: a str like '   <OPCODE>OP_ADD'
    """
    tmp='   '
    try:
        # for i in xml_list:
        #     if(i!=None):
        #         if(i!='\n'):
        #             tmp=tmp+i
        if(xml_list[0]!=None):
            if(xml_list[1]!=None):
                if(not xml_list[1].startswith('\n')):
                    tmp='   <'+xml_list[0]+'>'+xml_list[1]
                else:
                    tmp='   <'+xml_list[0]+'>'
            else:
                tmp = '   <' + xml_list[0] + '>'
        return tmp
    except:
        if (xml_list[0] != None):
            if (xml_list[1] != None):
                if(not xml_list[1].startswith('\n')):
                    return xml_list[0]+xml_list[1]
                else:
                    return '   <'+xml_list[0]+'>'
            else:
                return xml_list[0]
        else:
            return "**error**: List is NULL"


def compare_list(list1,list2,diff_position,txid,ret_list):
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
            else:
                pass
            tmp=list1[diff_position]+" -- "+list2[diff_position]
            output=list1
            output[diff_position]=tmp
        else:
            pass

        if(len(output)!=0):
            ret_list.append(output)
    except:
        print(" From compare_list Except......")
        print(list1)
        print(list2)

def record_len_not_equal_handler(txid):
    s="\n<TXID>"+str(txid)+'\n'+"**error**: The record length is not equal"
    return s

def compare_record(record_list1,record_list2,txid):
    """
    param:
        record_list: a record, list of list 
                     representing a record
                     made up of line_lists
    output:
        a list of list
    """
    ret_list=[]

    len1=len(record_list1)
    len2=len(record_list2)

    if(len1!=len2):
        ret_list.append(record_len_not_equal_handler(txid))
        ret_list.append("\nFile_a record is:\n")
        # ret_list.append(record_list1)
        for l in record_list1:
            ret_list.append(str_xml_list(l))
        ret_list.append("\nFile_b record is:\n")
        # ret_list.append(record_list2)
        for l in record_list2:
            ret_list.append(str_xml_list(l))
    else:   # comare if line number is the same
        # min_len=min({len1,len2})

        for i in range(1,len1):
            if i!=3:
                # compare if tag is the same
                if(record_list1[i][0]==record_list2[i][0]):
                    # the same tag
                    compare_list(record_list1[i],record_list2[i],1,txid,ret_list)
                    # if(compare_result!=None):
                    #     if(len(compare_result)!=0):
                    #         ret_list.append(compare_result)
                else:
                    # severe error: the tag is not the same on same number of lines
                    ret_list.append(["**error**: Tag Not The Same! \n    Tag1:"])
                    ret_list.append(str_xml_list(record_list1[i]))
                    ret_list.append(["    Tag2:"])
                    ret_list.append(str_xml_list(record_list2[i]))
            else:
                pass
    
    return ret_list

def write_file(result):
    """
    Result: a list starts with the TXID
            Format: [ <int>, <list>[ ],<list>[ ] ]
    """
    fp = open("output", 'w+')

    int_type=type(int(1))
    list_type=type(list())

    for record in result:
        for i in record:
            try:
                if(i!=None):
                    if(type(i)==int_type):
                        fp.write('\n')
                        fp.write("<TXID>"+str(i)+'\n')
                    else:
                        for x in i:
                            if (x != None and len(x)!=0):
                                fp.write(x)
                        fp.write('\n')

                # elif(len(i)==2):
                #     if(i[1]==None):
                #         tmp=" ** text is none ** "
                #     elif(i[0]!=None and i[1]!=None):
                #         tmp='  ' + i[0] + ' ' + i[1] + '\n'
                #     fp.write()
                # elif(len(i)==1):
                #     if(type(i)==list_type):
                #         fp.write(i[0]+'\n')
                #     else:
                #         fp.write(i+'\n')
            except:
                for a in i:
                    for x in a:
                        if(x!=None and len(x)!=0):
                            fp.write(x)
                    fp.write('\n')
                fp.write('\n')
                # print(i)

    fp.close()


def compare_files_by_records(file1_list,file2_list):
    """
    Compare two files of format： list[ record_list [ str_list ] ]
    """

if __name__=='__main__':
    file1 = 'a.xml'
    file2 = 'b.xml'


    file1_list=getXmlData(file1)

    file2_list=getXmlData(file2)

    result=list()
    #
    len1=len(file1_list)
    len2=len(file2_list)

    if(len1!=len2):
        result.append(["Warning: Number of RECORDS is not the same! \n"])
        result.append(["File 1 Len= "+ str(len1)])
        result.append(["File 2 Len= "+ str(len2)])

    # len_min=min({len1,len2})
    
    i=1 # discard the first record
    j=1
    while(i<len1 and j<len2):
        # first, get TXID
        list_a=file1_list[i]
        list_b=file2_list[j]


        # todo: txid may not be the 4th line
        txid_1=int(list_a[3][1])
        txid_2=int(list_b[3][1])

        if(txid_1==txid_2):
            tmp=compare_record(list_a,list_b,txid_1)
            if(tmp!=None):
                if(len(tmp)!=0):
                    result.append(tmp)
            i+=1
            j+=1
        elif(txid_1>txid_2):
            # write this to diff
            result.append(["Missing A RECORD from file1..."])
            result.append(list_a[3])
            j+=1
        elif(txid_1<txid_2):
            # write this to diff
            result.append(["Missing A RECORD from file2..."])
            result.append(list_b[3])
            i+=1
        else:
            print("else from main...\n")
            print(txid_1)
            print(txid_2)
            i += 1
            j += 1
        
    # print(result)

    write_file(result)
    

