import xmltodict


my_xml = """
    <audience>
      <id>what="attribute",123</id>
      <name>Shubham </name>
    </audience>
"""
a_xml="""
<RECORD>
    <OPCODE>OP_START_LOG_SEGMENT</OPCODE>
    <DATA>
      <TXID>132898</TXID>
    </DATA>
  </RECORD>
"""

weijin_dict=xmltodict.parse(my_xml)
# weijin_dict=xmltodict.parse(r"A:\Documents\Github Projects\DBB_Python\a.xml")
# with open(r"A:\Documents\Github Projects\DBB_Python\a.xml") as xml_file:
#   weijin_dict=xmltodict.parse(xml_file.read())

print(weijin_dict.items())