import sys
import codecs
import os
import django
from django.conf import settings
from django.core.management import call_command
from io import StringIO
from datetime import datetime

# setup access to django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rlb.settings")
django.setup()

# the actual export command


def do_work():
    # print(u"\xd6sterreich")
    call_command('dumpdata', use_natural_keys=True, use_natural_foreign_keys=True,
                 use_natural_primary_keys=True, format='xml', indent=2)

# nasty hack to workaround encoding issues on windows
_stdout = sys.stdout
sys.stdout = StringIO()
do_work()

value = sys.stdout.getvalue().decode('utf-8')
sys.stdout = _stdout

with codecs.open('export_{}.xml'.format(datetime.now().strftime("%Y-%m-%d_%H-%M")), 'w', 'utf-8-sig') as f:
    f.write(value)

print("export completed")
