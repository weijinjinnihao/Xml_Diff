import xml.etree.ElementTree as ET
import time
import ssh

ignore_list = ['TIMESTAMP', 'MTIME', 'ATIME']
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
                    tmp = '   <' + xml_list[0] + '>: ' + xml_list[1]
                else:
                    if (xml_list[0] == "DATA"):
                        tmp = ''
                    else:
                        tmp = '   <' + xml_list[0] + '>: '
            else:
                tmp = '   <' + xml_list[0] + '>: '
        return tmp
    except:
        if (xml_list[0] != None):
            if (xml_list[1] != None):
                if (not xml_list[1].startswith('\n')):
                    return xml_list[0] + xml_list[1]
                else:
                    return '   <' + xml_list[0] + '>: '
            else:
                return xml_list[0]
        else:
            return "**error**: List is NULL"

# def write_file(node1, node2, now, result):
#     """
#     Result: a list starts with the TXID
#             Format: [ <int>, <list>[ ],<list>[ ] ]
#     """
#     fp = open(node1 + "_VS._" + node2 + "_time_" + now + ".txt", 'w+')
#
#     int_type = type(int(1))
#     list_type = type(list())
#
#     for record in result:
#         for i in record:
#             try:
#                 if (i != None):
#                     if (type(i) == int_type):
#                         fp.write('\n')
#                         fp.write("<TXID>" + str(i) + '\n')
#                     else:
#                         for x in i:
#                             if (x != None and len(x) != 0):
#                                 fp.write(x)
#                         fp.write('\n')
#
#                 # elif(len(i)==2):
#                 #     if(i[1]==None):
#                 #         tmp=" ** text is none ** "
#                 #     elif(i[0]!=None and i[1]!=None):
#                 #         tmp='  ' + i[0] + ' ' + i[1] + '\n'
#                 #     fp.write()
#                 # elif(len(i)==1):
#                 #     if(type(i)==list_type):
#                 #         fp.write(i[0]+'\n')
#                 #     else:
#                 #         fp.write(i+'\n')
#             except:
#                 for a in i:
#                     for x in a:
#                         if (x != None and len(x) != 0):
#                             fp.write(x)
#                     fp.write('\n')
#                 fp.write('\n')
#                 # print(i)
#
#     fp.close()
if __name__ == '__main__':
    ip1 = '192.168.0.41'
    ip2 = '192.168.0.42'
    ip3 = '192.168.0.44'
    username = 'root'
    password = '111111'
    port = 22
    ssh.get3str(ip1,ip2,ip3, username, password, port)

    node1_name = "NN41"
    node2_name = "NN42"
    node3_name = "NN44"
    file1 = "/home/weijin/nn1_41.xml"
    file2 = "/home/weijin/nn2_42.xml"
    file3 = "/home/weijin/nn3_44.xml"


    file1_list = getXmlData(file1)

    file2_list = getXmlData(file2)

    file3_list = getXmlData(file3)

    result = list()
    #
    len1 = len(file1_list)
    len2 = len(file2_list)
    len3 = len(file3_list)



    result.append("The length of Record of " + node1_name + ": " + str(len1))
    result.append("The range of Record's TXID of " + node1_name + ": " + '['+ file1_list[0][3][1] + "," +
                   file1_list[-1][3][1] + ']')
    result.append("The length of Record of " + node2_name + ": " + str(len2))
    result.append("The range of Record's TXID of " + node2_name + ":" + '[' + file2_list[0][3][1] + "," +
                   file2_list[-1][3][1] + ']')
    result.append("The length of Record of " + node3_name + ": " + str(len3))
    result.append("The range of Record's TXID of " + node3_name + ":" + '['+ file3_list[0][3][1] + "," +
                   file3_list[-1][3][1] + ']')


    for l in result:
        print(l)
    # now = time.strftime("%m_%d_%H_%M_%S")
    # write_file(node1_name, node2_name, now, result)