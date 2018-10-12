import xml.etree.ElementTree as ET

# for each node of root
# append the line to list
line_id = 0
def walkData(root_node, result_list,ignore_list):
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
    if (len(children_node) == 0):
        return
    for child in children_node:
        walkData(child, result_list,ignore_list)
    return


# in:
#   a file
# out:
#   records_list: a list of records
#   record is a list of lines
def getXmlData(file_name,ignore_list):
    # level = 1 #节点的深度从1开始
    result_list = []
    root = ET.parse(file_name).getroot()
    # walkData(root, level, result_list)
    walk_data_by_records(root, result_list, ignore_list)
    return result_list


def walk_data_by_records(root_node, result_list,ignore_list):
    record_list = []
    root_tag = root_node.tag
    if (root_tag == 'RECORD'):
        # this is a records node
        # should return a list of this record

        # line id
        global line_id
        line_id = 0
        walkData(root_node, record_list,ignore_list)

        result_list.append(record_list)
    elif (root_tag == 'EDITS'):
        children_node = root_node.getchildren()

        if (len(children_node) == 0):
            return
        for child in children_node:
            walk_data_by_records(child, result_list,ignore_list)
    else:
        pass

