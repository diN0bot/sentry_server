import os, sys

sys.path.append('/data/sentry')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

# Django's default for MySQL causes a ping() call many times when it isn't needed.
#
# We are dynamically patching the class object, so we don't need to patch django itself.
#
# See for more background:
#  <http://www.mail-archive.com/django-developers@googlegroups.com/msg19109.html>
def django_patcher():
  from django.db.backends.mysql import base
  def valid_connection_replacement(self):
    return self.connection is not None
  base.DatabaseWrapper._valid_connection = valid_connection_replacement

django_patcher()

application = django.core.handlers.wsgi.WSGIHandler()
