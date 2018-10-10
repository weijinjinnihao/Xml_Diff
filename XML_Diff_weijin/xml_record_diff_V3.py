# -*- coding: UTF-8 -*-

# change:
#   add IF print different records
#   add line number to record

import xml.etree.ElementTree as ET
import time

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
            return "**error**: List is NULL"


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
            tmp=' ('+node1_name+')  '+list1[diff_position]+" -- "+'('+node2_name+')'+list2[diff_position]
            head='  ('+'Line Number: '+str(list1[2])+')'+'<'+list1[0]+'>'
            output=head+tmp
        else:
            pass

        if(len(output)!=0):
            ret_list.append(output)
    except:
        print(" From compare_list Except......")
        print(list1)
        print(list2)

def compare_list_same(list1,list2,same_position,txid,ret_list):
    """
    compare two list on given rules
    out:
        append a list to ret_list which will be written into files
        output only if different
        output a list containing the difference info
    """
    output=list()

    try:
        if(list1[same_position]==list2[same_position]):
            # wtite txid only once for each record

            tmp=' ('+node1_name+')'+' ('+node2_name+')'+' '+list1[same_position]
            head='  ('+'Line Number: '+str(list1[2])+')'+'<'+list1[0]+'>'
            output=head+tmp

        else:
            pass

        if(len(output)!=0):
            ret_list.append(output)
    except:
        print(" From compare_list Except......")
        print(list1)
        print(list2)

def record_len_not_equal_handler(txid):
    s = "\n<TXID>" + str(txid) + '\n' + "\n**  error**: The record length is not equal!"
    return s


def compare_record(record_list1, record_list2, txid,To_see_record_same):
    """
    param:
        record_list: a record, list of list
                     representing a record
                     made up of line_lists
    output:
        a list of list
    """
    # ret_list_diff=[]
    ret_list = []

    len1 = len(record_list1)
    len2 = len(record_list2)

    if (len1 != len2):
        ret_list.append(record_len_not_equal_handler(txid))
        # ret_list.append(record_list1)
        for l in record_list1:
            s= str_xml_list(l)
            if (len(s) != 0):
                ret_list.append(s)
        ret_list.append("\n" + node2_name + " record is:\n")
        # ret_list.append(record_list2)
        for l in record_list2:
            s = str_xml_list(l)
            if (len(s) != 0):
                ret_list.append(s)
    else:  # comare if line number is the same
        # min_len=min({len1,len2})
        if  ((To_see_record_same == 'n') or (To_see_record_same == 'N')):
            for i in range(1, len1):
                if i != 3:
                    # compare if tag is the same
                    if (record_list1[i][0] == record_list2[i][0]) :

                        compare_list_diff(record_list1[i], record_list2[i], 1, txid, ret_list)

                    else:
                        # severe error: the tag is not the same on same number of lines
                        ret_list.append(["\n  **error**: Tag Not The Same!"])
                        tmp = "     (Line Number: " + str(record_list1[i][2]) + ') (' + node1_name + ') '
                        tmp += str_xml_list(record_list1[i])[3:]
                        # ret_list.append(tmp)
                        # ret_list.append(["    Tag of : "+node2_name])
                        tmp += " -- " + '(' + node2_name + ') '
                        tmp += str_xml_list(record_list2[i])[3:]
                        ret_list.append(tmp)
                else:
                    pass
        else:
            for i in range(1, len1):
                if i != 3:
                    if (record_list1[i][0] == record_list2[i][0]) :
                        compare_list_diff(record_list1[i], record_list2[i], 1, txid, ret_list)

                    else:
                        # severe error: the tag is not the same on same number of lines
                        ret_list.append(["\n  **error**: Tag Not The Same!"])
                        tmp = "     (Line Number: " + str(record_list1[i][2]) + ') (' + node1_name + ') '
                        tmp += str_xml_list(record_list1[i])[3:]
                        # ret_list.append(tmp)
                        # ret_list.append(["    Tag of : "+node2_name])
                        tmp += " -- " + '(' + node2_name + ') '
                        tmp += str_xml_list(record_list2[i])[3:]
                        ret_list.append(tmp)
                else:
                    pass
            if (len(ret_list)!=0):
                ret_list.append("The Same Part:\n")
                for i in range(1, len1):
                    if i != 3:
                        # compare if tag is the same
                        if (record_list1[i][0] == record_list2[i][0]) :

                            compare_list_same(record_list1[i], record_list2[i], 1, txid, ret_list)
                        else:
                            pass
                    else:
                        pass
    return ret_list


def write_file(node1, node2, now, result):
    """
    Result: a list starts with the TXID
            Format: [ <int>, <list>[ ],<list>[ ] ]
    """
    fp = open(node1 + "_VS._" + node2 + "_time_" + now + ".txt", 'w+')

    int_type = type(int(1))
    list_type = type(list())

    for record in result:
        for i in record:
            try:
                if (i != None):
                    if (type(i) == int_type):
                        fp.write('\n')
                        fp.write("<TXID>" + str(i) + '\n')
                    else:
                        for x in i:
                            if (x != None and len(x) != 0):
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
                        if (x != None and len(x) != 0):
                            fp.write(x)
                    fp.write('\n')
                fp.write('\n')
                # print(i)

    fp.close()


def compare_files_by_records(file1_list, file2_list):
    """
    Compare two files of format： list[ record_list [ str_list ] ]
    """


if __name__ == '__main__':
    node1_name = "NN41"  # file1
    node2_name = "NN42" # file2

    if node1_name == "NN41":
        file1 = "a.xml"
    elif node1_name == "NN42":
        file1 = "b.xml"
    elif node1_name == "NN44":
        file1 = "c.xml"

    if node2_name == "NN41":
        file2 = "a.xml"
    elif node2_name == "NN42":
        file2 = "b.xml"
    elif node2_name == "NN44":
        file2 = "c.xml"

    To_see_record_same = input("Do you want to see the same Tags? [y/n]")

    file1_list = getXmlData(file1)

    file2_list = getXmlData(file2)

    result = list()
    #
    len1 = len(file1_list)
    len2 = len(file2_list)

    result.append(["The length of Record of two nodes:\n"])
    if (len1 != len2):
        result.append(["    The length of Record:  not the same!\n"])
        result.append(["    The length of Record of " + node1_name + ": " + str(len1)])
        result.append(["    The range of Record's TXID of " + node1_name + ": " + "[" + file1_list[0][3][1] + "," +
                       file1_list[-1][3][1] + "]"])
        result.append(["    \n"])
        result.append(["    The length of Record of " + node1_name + ": " + str(len2)])
        result.append(["    The range of Record's TXID of " + node1_name + ":" + "[" + file2_list[0][3][1] + "," +
                       file2_list[-1][3][1] + "]"])
    else:
        result.append(["    The length of Record:  same" + "=" + str(len1)])
    result.append(["\n"])
    result.append(["ignore list : \n"])
    for ign in ignore_list:
        result.append(["    " + ign])
    # len_min=min({len1,len2})

    i = 1  # discard the first record
    j = 1
    while (i < len1 and j < len2):
        # first, get TXID
        list_a = file1_list[i]
        list_b = file2_list[j]

        # todo: txid may not be the 4th line
        txid_1 = int(list_a[3][1])
        txid_2 = int(list_b[3][1])

        if (txid_1 == txid_2):
            tmp = compare_record(list_a, list_b, txid_1,To_see_record_same)
            if (tmp != None):
                if (len(tmp) != 0):
                    result.append(tmp)
            i += 1
            j += 1
        elif (txid_1 > txid_2):
            # write this to diff
            result.append(["Missing A RECORD from file1..."])
            result.append(list_a[3])
            j += 1
        elif (txid_1 < txid_2):
            # write this to diff
            result.append(["Missing A RECORD from file2..."])
            result.append(list_b[3])
            i += 1
        else:
            print("else from main...\n")
            print(txid_1)
            print(txid_2)
            i += 1
            j += 1

    # print(result)
    now = time.strftime("%m_%d_%H_%M_%S")
    write_file(node1_name, node2_name, now, result)


