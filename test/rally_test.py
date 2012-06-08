#!/opt/local/bin/python2.6

#################################################################################################
#
# getitem.py -- Get info for a specific instance of a Rally type
#               identified by a FormattedID value
#
USAGE = """
Usage: getitem.py <FormattedID>    
"""
#################################################################################################

import sys
import re
import string

from pyral import Rally, rallySettings

#################################################################################################

errout = sys.stderr.write

ARTIFACT_TYPE = { 'DE' : 'Defect',
                  'TA' : 'Task',
                  'TC' : 'TestCase',
                  'US' : 'HierarchicalRequirement',
                  'S'  : 'HierarchicalRequirement',
                  }

FORMATTED_ID_PATT = re.compile(r'(?P<prefix>[A-Z]+)\d+')

COMMON_ATTRIBUTES = ['_type', 'oid', '_ref', '_CreatedAt', '_hydrated', 'Name']

##################################################################################################

PREVIEW = "preview.rallydev.com"
DEMO    = "demo.rallydev.com"
PROD    = "rally1.rallydev.com"

PREVIEW_USER = "usernumbernine@acme.com"
PREVIEW_PSWD = "********"

PROD_USER = "house.li@myriadgroup.com"
PROD_PSWD = "@Lenciel1"
#################################################################################################
def basic_connection():
    """
        Using a known valid Rally server and access credentials, issue a simple query
        request against a known valid Rally entity.
    """
    rally = Rally(server=PROD, user=PROD_USER, password=PROD_PSWD)
    response = rally.get('Project', fetch=False, limit=10)
    print response

def main():

    server='rally1.rallydev.com'
    user='House.Li@myriadgroup.com'
    password='@Lenciel1'
    #workspace=
    #project = rallySettings(options)
    #print " ".join(["|%s|" % item for item in [server, user, '********', workspace, project]])
    rally = Rally(server, user, password)      # specify the Rally server and credentials
    rally.enableLogging('rally.hist.item') # name of file you want logging to go to

    if len(args) != 1:
        errout(USAGE)
        sys.exit(2)
    ident = 3726723403

    mo = FORMATTED_ID_PATT.match(ident)
    if mo:
        ident_query = 'FormattedID = "%s"' % ident
        entity_name = ARTIFACT_TYPE[mo.group('prefix')]
    else:
        errout('ERROR: Unable to determine ident scheme for %s\n' % ident)
        sys.exit(3)

    response = rally.get(entity_name, fetch=True, query=ident_query)

    if response.errors:
        errout("Request could not be successfully serviced, error code: %d\n" % response.status_code)
        errout("\n".join(response.errors))
        sys.exit(1)

    if response.resultCount == 0:
        errout('No item found for %s %s\n' % (entity_name, ident))
        sys.exit(4)
    elif response.resultCount > 1:
        errout('WARNING: more than 1 item returned matching your criteria\n')

    for item in response:
        for attr in COMMON_ATTRIBUTES:
            print "    %-16.16s : %s" % (attr, getattr(item, attr))
        attrs = [attr for attr in item.attributes() if attr not in COMMON_ATTRIBUTES]
        for attr in sorted(attrs):
            attribute = getattr(item, attr)
            cn = attribute.__class__.__name__
            if cn[0] in string.uppercase:
                attribute = attribute.Name if cn != 'NoneType' else None
            print "    %-16.16s : %s" % (attr, attribute)

#################################################################################################
#################################################################################################

if __name__ == '__main__':
    basic_connection()
