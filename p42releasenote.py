# -*- coding: UTF-8 -*-
'''
Created on June 7, 2012

@author: House.Li

This is for abstracting information from perforce then generate a release note automatically
'''
import os

from django.template.loader import render_to_string
from django.conf import settings

from lxml.html.clean import Cleaner
import lxml.html as H
import lxml.etree as ET

from P4 import P4, P4Exception

import re;
import sys;
import time;
import datetime;
import string;
import traceback;
import ConfigParser
import logging

from change import *

class AP4:
    '''
    P4 wrapper class to expose APIs we used
    '''
    def __init__( self, ini_file ):
        '''
        Initialization
        '''

        #start logger
        #self.create_logger();

        #create p4 proxy object
        self.p4 = P4()

        #load config
        self.ini_file = ini_file
        self.load_cfg()

        #init as append mode
        self.append = True

    def load_cfg(self):
        '''
        load configuration from the ini file
        '''
        self.config = ConfigParser.ConfigParser()
        self.config.readfp( open( self.ini_file ) )
#        self.new_label = self.config.get( "Label", "new" )
#        self.old_label = self.config.get( "Label", "old" )
        self.p4.port = self.config.get( "Server", "port" )
        self.p4.user = self.config.get( "Server", "user" )
        self.p4.password = self.config.get( "Server", "password" )
        self.p4.client = self.config.get( "Server", "client" )

    def create_logger(self):
        '''
        create the logger
        '''
        log_filename = ( time.strftime( 'P4Python.%Y%m%dT%H%M%S.log', time.gmtime( time.time() ) ) )
        logging.basicConfig( level = logging.INFO,
            filename = log_filename,
            filemode = 'a' )

        self.logger = logging.getLogger( "p4 pyclient logger" )
        #ch = logging.StreamHandler()
        ch = logging.FileHandler( log_filename )
        ch.setLevel( logging.INFO )
        ch.setFormatter( logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s \r\n %(message)s' ) )
        self.logger.addHandler( ch )

    def log_exception( self ):
        type, val, tb = sys.exc_info()
        #self.logger.error( string.join( traceback.format_exception( type, val, tb ), '' ) )
        print string.join( traceback.format_exception( type, val, tb ), '' )
        del type, val, tb

    def log_message( self, msg ):
        #self.logger.info( msg )
        print msg

    def check_version( self ):
        '''
        check the version number in pom.xml
        '''
        pom = self.config.get('Version', 'pom_path')
        current_ver = ET.ElementTree(file=pom).findtext("{http://maven.apache.org/POM/4.0.0}version")
        #print current_ver
        latest_ver = self.config.get('Version', 'new')
        #print latest_ver
        if current_ver != latest_ver:
            self.append = False
            self.config.set('Version', 'old', latest_ver)
            self.config.set('Version', 'new', current_ver)
            with open(self.ini_file, 'w') as configfile:
                self.config.write(configfile)

    def get_connectionInfo( self ):
        '''
        Get the connection info by running "p4 info" (returns a dict)
        '''
        info = self.p4.run( "info" )
        for key in info[0]:
            self.log_message("%s=%s" % (key , info[0][key]))

    def diff_between_labels( self ):
        self.bug_fixings = []
        self.features = []
        self.improvements = []
        '''
        get the diff change information between two different labels
        '''
        with self.p4.at_exception_level( P4.RAISE_ERRORS ): # to ignore "File(s) up-to-date"
            try:
                #get the changes list between two labels
                if self.append:
                    old_label = "Ver_%s" % self.config.get("Version", 'new')
                    new_label = "now"
                else:
                    old_label = "Ver_%s" % self.config.get("Version", 'old')
                    new_label = "Ver_%s" % self.config.get("Version", 'new')
                change_dict_list = self.p4.run( "changes", "-l", "-i",
                    "//Products/uiActive/Client/java/UIFramework/Android/Pivot/...@%s,@%s"
                    % ( old_label, new_label ) )
             
                #print self.config.get("Version",'new')
                self.release_ver = "Ver_%s" % self.config.get("Version", 'new')
                #print self.release_ver

                self.log_message("-----------------START-----------------------")
                if len(change_dict_list)>0:
                    for change_dict in change_dict_list:
                        change_time =  datetime.datetime.utcfromtimestamp(int(change_dict['time']))
                        self.log_message( change_dict['user'] )
                        self.log_message( change_time )
                        self.log_message( change_dict['change'])
                        desc = change_dict['desc']

                        list = re.findall(r'^\[(.*)\](.*)', desc, re.M)
                        new_list = []
                        if len(list)>0:
                            for item in list:
                                linkPattern = re.compile(r'\W+(\w.*)', re.S)
                                m = re.match(linkPattern, item[1])
                                if m:
                                    new_list.append((item[0],m.group(1)))
                                else:
                                    new_list.append((item[0],item[1]))
                        if len(new_list)>0:
                            if new_list[0][0] == "Feature":
                                 f = Feature()
                                 f.title = new_list[0][1]
                                 f.desc = new_list[2][1]
                                 f.change_number = change_dict['change']
                                 f.rb_link = new_list[4][1]
                                 f.us_number = new_list[1][1]
                                 self.features.append(f)
                            elif list[0][0] == "Bug Fixing":
                                 b = Defect()
                                 b.title = new_list[0][1]
                                 b.desc = new_list[2][1]
                                 b.change_number = change_dict['change']
                                 b.rb_link = new_list[4][1]
                                 b.defect_number = new_list[1][1]
                                 self.bug_fixings.append(b)
                            elif list[0][0] == "Improvement":
                                 i = Change()
                                 i.title = new_list[0][1]
                                 i.desc = new_list[2][1]
                                 i.change_number = change_dict['change']
                                 i.rb_link = new_list[4][1]
                                 self.improvements.append(i)
                            else:
                                print "Ignore this change"
                        else:
                            print 'No match'
                else:
                    self.log_message("no change found between the current release to the previous release")
                self.log_message("-----------------END-----------------------")
            except P4Exception:
                self.log_exception()
                for e in self.p4.errors:
                    self.log_message( "Error:" + e )
                for e in self.p4.warnings:
                    self.log_message( "Warning:" + e )
                    self.log_message( e )

    def create_changelist( self, change_desc, file_list ):
        '''
        Create a new changelist with given change_desc and file_list
        '''
        self.change = self.p4.fetch_change()
        self.change._description = change_desc
        self.change._files = file_list
        #print change

    def connect(self):
        '''
        Connect to the P4 Server
        '''
        try:
            self.p4.connect()
        except P4Exception:
            self.log_exception()
            for e in self.p4.errors: # Display errors
                self.log_message( "Error:" + e )
            sys.exit( 1 )

    def disconnect( self ):
        '''
        Disconnect from the P4 Server
        '''
        self.p4.disconnect()

if __name__ == '__main__':
    ap4 = AP4( 'cfg.ini' )
    ap4.connect()
    #ap4.get_connectionInfo()
    ap4.check_version()
    ap4.diff_between_labels()
    ap4.disconnect()

    SETTINGS_DIR = os.path.dirname( os.path.realpath( __file__ ) )
    settings.configure(TEMPLATE_DIRS = (os.path.join( SETTINGS_DIR, "templates" ),))

    rendered = render_to_string('my_template.html', {"version_number": ap4.release_ver,
                                                     "defects" : ap4.bug_fixings,
                                                     "features" : ap4.features,
                                                     "improvements" : ap4.improvements})


    new_section = H.document_fromstring(rendered)
    bytes_in = H.tostring(new_section, pretty_print=True, encoding=unicode)
    new_section_str=Cleaner().clean_html(bytes_in).encode('utf-8')

    old_report = 'templates/old.html'
    new_report = 'templates/new.html'
    tree = ET.parse(old_report, ET.HTMLParser())
    release_div = tree.find(".//div[@id='release']")
    body = release_div.getparent()
    if ap4.append:
        body.replace(release_div, ET.HTML(new_section_str))
    else:
        body.insert(body.index(release_div), ET.HTML(new_section_str))
    f = open( new_report, "w")
    f.write(ET.tostring(tree, pretty_print=True, method="html"))
    f.close()
