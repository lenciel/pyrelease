# -*- coding: UTF-8 -*-
'''
Created on June 7, 2012

@author: House.Li

Container for the change objects
'''


class Change(object):
    '''
    Base class for all changes
    '''
    def __init__(self, title=None, change_number=None, desc=None, rb_link=None):
        self._title = title;
        self._change_number = change_number;
        self._desc = desc;
        self._rb_link = rb_link;

    def get_title(self):
        return self._title
    def set_title(self, value):
        self._title = value
    title = property(get_title, set_title)

    def get_change_number(self):
        return self._change_number
    def set_change_number(self, value):
        self._change_number = value
    change_number = property(get_change_number, set_change_number)

    def get_desc(self):
        return self._desc
    def set_desc(self, value):
        self._desc = value
    desc = property(get_desc, set_desc)

    def get_rb_link(self):
        return self._rb_link
    def set_rb_link(self, value):
        self._rb_link = value
    rb_link = property(get_rb_link, set_rb_link)

class Feature(Change):
    '''
    A feature is a change with valid User story id in rally
    '''
    def __init__(self, us_number=None):
        self._us_number = us_number

    def get_us_number(self):
        return self._us_number
    def set_us_number(self, value):
        self._us_number = value
    us_number = property(get_us_number, set_us_number)

class Defect(Change):
    '''
    A defect fixing is a change with valid defect number in rally
    '''
    def __init__(self, defect_number=None):
        self._defect_number = defect_number

    def get_defect_number(self):
        return self._defect_number
    def set_defect_number(self, value):
        self._defect_number = value
    defect_number = property(get_defect_number, set_defect_number)

if __name__ == '__main__':

    c = Change()
    c.desc = "hha"
    print c.desc
    c.desc = "bbbb"
    print c.desc

    d = Defect()
    d.desc = "hhhh"
    print d.desc
    d.desc = "aaaaa"
    print d.desc

    d.defect_number = "1231312"
    print d.defect_number
