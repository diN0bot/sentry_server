from django.conf import settings
from settings import pathify
from django.conf.urls.defaults import *

import os

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',)

urlpatterns += patterns('',
  (r'^sentry/', include('sentry.urls')),

  (r'^admin/doc/', include('django.contrib.admindocs.urls')),
  url(r'^admin/(.*)', include(admin.site.urls), name="admin"),
)

if settings.DJANGO_SERVER:
  urlpatterns += patterns('',
    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
  )
"""
urlpatterns += patterns('',
  # static pages that still work when database is offline
  (r'^', include('procrasdonate.views.static_urls')),
)

if settings.DOWN_FOR_MAINTENANCE:
  urlpatterns += patterns('',
    (r'^.*', 'django.views.generic.simple.direct_to_template', { 'template': 'procrasdonate/down_for_maintenance.html' }),
  )

#urlpatterns += patterns('',
#)

"""

CUSTOM_URLS_APPS = ()

for app in settings.APPS:
  if app not in CUSTOM_URLS_APPS and os.path.exists(pathify([settings.PROJECT_PATH, app, 'views'])):
    urlpatterns += patterns('',
      (r'^%s/' % app, include('%s.views.urls' % app)),
    )
