import os
def path(p):
  """
  @param p: path with *nix path separator
  @return: string with os-specific path separator
  """
  return os.sep.join(p.split("/"))

import re
_space_replace = re.compile("([^\\\])( )")
def pathify(lst, file_extension=False):
  """
  @param lst: list of path components
  @return: string with os-specific path separator between components
  """
  # replaces spaces with raw spaces so that spaces in file names work
  repl = r"\g<1> "
  return os.sep.join([_space_replace.sub(repl, el) for el in lst])
  #if file_extension:
  #  return os.sep.join([el != lst[-1] and _space_replace.sub(repl, el.replace('.', os.sep)) or _space_replace.sub(repl, el) for el in lst])
  #else:
  #  return os.sep.join([_space_replace.sub(repl, el.replace('.', os.sep)) for el in lst])

import sys
if not sys.stdout:
  # fail on windows?
  #sys.stdout = file(path('/dev/null'),"w")
  sys.stdout = file(path('/var/log/apache2/whynoti.org/stdout.log'),"a")

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

DEBUG = False # True for general debug mode, eg, will display debug info rather than 404 or 500
DJANGO_SERVER = False # True if using django's runserver
TEMPLATE_DEBUG = DEBUG # Template exceptions won't crash rendering, plus mroe useful exception message is shown in console.
DEBUG_SQL = DEBUG

ADMINS = (
  ('testing123', 'lucy@cloudkick.com')
)
MANAGERS = ADMINS

APPS = ()

try:
  # specify APPS here
  from local_presettings import *
except:
  pass

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

ROOT_URLCONF = 'urls'

# check this out: http://www.djangosnippets.org/snippets/1068/

# Absolute path to the directory that holds media.
# including upload image directory
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = pathify([PROJECT_PATH, path('site_media/')])

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/site_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'overwrite this in local_settings.py'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.load_template_source',
  'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
  # required to turn localization on per user
  'django.middleware.gzip.GZipMiddleware',
  #'cloudkick.webapp.account.middleware.PerUserLocaleMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.locale.LocaleMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.doc.XViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  #'django.contrib.csrf.middleware.CsrfMiddleware',
  #'lib.ssl_middleware.SSLRedirect',
)
for app in APPS:
  if os.path.exists(pathify([PROJECT_PATH, app, 'middleware.py'], file_extension=True)):
    MIDDLEWARE_CLASSES += (
      '%s.middleware.%sMiddleware' % (app, app.capitalize()),
    )

#if DEBUG_TOOLBAR:
#  MIDDLEWARE_CLASSES += (
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
#  )

TEMPLATE_DIRS = (
  pathify([PROJECT_PATH, path('webapp/templates/')]),
)

for app in APPS:
  if os.path.exists(pathify([PROJECT_PATH, app, 'templates'])):
    TEMPLATE_DIRS += (
      pathify([PROJECT_PATH, path('%s/templates' % app)]),
    )

INSTALLED_APPS = (
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.humanize',
  'django.contrib.auth',
  'django.contrib.admindocs',
  'django.contrib.admin',

  'south',

  'indexer',
  'paging',
  'sentry',
  'sentry.client',
  'sentry.plugins.sentry_servers',
  'sentry.plugins.sentry_urls',
  'sentry.plugins.sentry_sites',
  'sentry.plugins.sentry_redmine',
)

SENTRY_REMOTE_TIMEOUT = 5
SENTRY_THRASHING_TIMEOUT = 0
SENTRY_TESTING = True
SENTRY_FILTERS = (
    'sentry.filters.StatusFilter',
    'sentry.filters.LoggerFilter',
    'sentry.filters.LevelFilter',
    'sentry.filters.ServerNameFilter',
    'sentry.filters.SiteFilter',
    #'example_project.filters.IPFilter',
)
SENTRY_SITE = 'ck'
SENTRY_PUBLIC = False
SENTRY_CATCH_404_ERRORS = True

for app in APPS:
  INSTALLED_APPS += (
    app,
  )


#USE_MARKUP = True
#if USE_MARKUP:
#  INSTALLED_APPS += ('django.contrib.markup',)

#if DEBUG_TOOLBAR:
#  INSTALLED_APPS += ('debug_toolbar',)

TEMPLATE_CONTEXT_PROCESSORS = (
  'django.core.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.core.context_processors.request',
)

for app in APPS:
  if os.path.exists(pathify([PROJECT_PATH, app, 'context.py'], file_extension=True)):
    TEMPLATE_CONTEXT_PROCESSORS += (
      '%s.context.defaults' % app,
    )

try:
  from local_settings import *
except:
  pass
