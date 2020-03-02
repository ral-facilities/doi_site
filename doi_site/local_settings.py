"""
Django local settings for doi_site project.

This file contains the variables that MAY/SHOULD be set with values specific for
the deployment.
"""

# Datacite URL, the default in settings.py is the test service
# Override here to use the production service
# DATACITE_URL = 'https://mds.datacite.org/'

# Datacite handler, the default in settings.py is the test service
# Override here to use the production service
# DATACITE_HANDLER = 'http://dx.doi.org/'

# Web proxy
# HTTP_PROXY_HOST = 'example.org'
# HTTP_PROXY_PORT = '8080'
import ldap
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True

# The organisation's DataCite prefix in the form nn.nnnn
DOI_PREFIX = 'nn.nnnn'

# The organisation's username for DataCite
DATACITE_USER_NAME = 'BL.XXXX'

# The organisation's password for DataCite
DATACITE_PASSWORD = 'xxxxxxxxxxxxxxxxx'

# The URI of the organisation's LDAP server
AUTH_LDAP_SERVER_URI = "ldap://fed.cclrc.ac.uk:389"

AUTH_LDAP_USER_SEARCH = LDAPSearch("DC=fed,DC=cclrc,DC=ac,DC=uk", ldap.SCOPE_SUBTREE, "(cn=%(user)s)")

# The organisation's LDAP DN template
# AUTH_LDAP_USER_DN_TEMPLATE = "CN=%(user)s,objectClass=*,DC=fed,DC=cclrc,DC=ac,DC=uk"

# The name of your organisation, this will be displayed on the home page
ORGANISATION_NAME = 'My Organisation'

# An email address for people to contact you about the this service, this will
# be displayed on the home page
ORGANISATION_DOI_EMAIL = 'doi@example.org'

# SECURITY WARNING: keep the secret key used in production secret!
# A secret key for a particular Django installation. This is used to provide
# cryptographic signing, and should be set to a unique, unpredictable value.
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# A list of strings representing the host/domain names that this Django site
# can serve
ALLOWED_HOSTS = [
    '127.0.0.1',
    'example.org',
    'localhost'
]

# The URL of the location of the document detailing users roles and
# responsibilities
ROLES_URL = 'https://example.org/DOI-responsibilities.docx'

# The URL of the location of the document containing notes for issuers
NOTES_URL = 'https://example.org/Notes%20for%20Issuers.docx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# DATABASES = { 'default': { 'ENGINE': 'django.db.backends.sqlite3', 'NAME': '/var/doi/doi.db' } }

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
                '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'mds': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django_auth_ldap': {
            'level': 'DEBUG',
            'handlers': ['console']}
        

    }
}

