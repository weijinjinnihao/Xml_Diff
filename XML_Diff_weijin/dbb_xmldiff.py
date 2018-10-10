
from lxml import etree
from xmldiff import main, formatting

unique_attr='TXID'
my_formatter=formatting.XMLFormatter()
diff = main.diff_files(left='aa.xml',right= 'bb.xml',uniqueattrs=unique_attr)#[DeleteNode(node='/RECORD/DATA/TIMESTAMP')]


print(diff)