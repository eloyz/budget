import os
import sys
from os.path import abspath, dirname, join
from site import addsitedir

sys.path.insert(0, abspath(join(dirname(__file__), "../../")))

from django.conf import settings

os.environ["DJANGO_SETTINGS_MODULE"] = "fudget.settings"
sys.path.insert(0, join(settings.PROJECT_ROOT))

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

