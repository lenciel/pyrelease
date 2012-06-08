import urllib2
import urllib
import lxml.html as H
import lxml.etree as ET
from lxml.html.clean import Cleaner
import re

if __name__ == '__main__':

    old_report = 'templates/old.html'
    new_report = 'templates/new.html'
    tree = ET.parse(old_report, ET.HTMLParser())
    release_div = tree.find(".//div[@id='release']")
    #print ET.tostring(release_div)
    body = release_div.getparent()
    #print ET.tostring(body)
    body.insert(body.index(release_div), ET.XML("<div style='clear:both'> </div>"))
#    feature = doc.get_element_by_id('feature')
    print ET.tostring(tree, pretty_print=True, method="html")

    # extract the links that we wantread()
#
#    doc = H.document_fromstring(site)
#    bytes_in = H.tostring(doc, pretty_print=True,encoding=unicode)
#    parsedContent=Cleaner().clean_html(bytes_in).encode('utf-8')
#    print(parsedContent)
#    pageLinkPattern = re.compile(r'\bviewthread\.php\?tid='+tid+'&extra=&page=(\d+)$', re.I)
#
#    f = open( new_report, "w")
#    f.write(bytes_in.encode('utf-8'))
#    f.close()