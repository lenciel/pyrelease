__author__ = 'House.Li'

import re



if __name__ == '__main__':
    text = "[Feature] add a new feature blablabla \n[Story/Defect id] US123456 \n[Description]: blablabla \n[Test]: test on device \n[ReviewBorad URL]: http://reviewboard.myriadgroup.com/r/33558/"
    list = re.findall(r'^\[(.*)\](.*)', text, re.M)
    if len(list)>0:
        print 'Match found: ', list
    else:
        print 'No match'

    linkPattern = re.compile(r'\W+(\w.*)', re.S)
    m = re.match(linkPattern, " : http://thisisa link")
    if m:
        print m.group(1)
    else:
        print "Not matched"
