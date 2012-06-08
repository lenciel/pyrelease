__author__ = 'House.Li'


import os

from django.template.loader import render_to_string
from django.conf import settings

if __name__ == '__main__':
#    ap4 = AP4( 'cfg.ini' )
#    ap4.connect()
#    ap4.get_connectionInfo()
#    ap4.diff_between_labels()
#    ap4.disconnect()
    SETTINGS_DIR = os.path.dirname( os.path.realpath( __file__ ) )
    settings.configure(
        TEMPLATE_DIRS = (
            os.path.join( SETTINGS_DIR, "templates" ),
            )) # We have to do this to use django templates standalone - see
    # http://stackoverflow.com/questions/98135/how-do-i-use-django-templates-without-the-rest-of-django

    rendered = render_to_string('my_template.html', {"version_number": "0.0.2"})
    print rendered