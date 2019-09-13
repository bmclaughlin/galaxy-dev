import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PULP_DB_NAME', 'pulp'),
        'USER': os.environ.get('PULP_DB_USER', 'pulp'),
        'PASSWORD': os.environ.get('PULP_DB_PASSWORD', ''),
        'HOST': os.environ.get('PULP_DB_HOST', 'localhost'),
        'PORT': os.environ.get('PULP_DB_PORT', ''),
    }
}

CONTENT_PATH_PREFIX = '/api/automation-hub/artifacts/collections/'

ANSIBLE_API_HOSTNAME = ''

MEDIA_ROOT = '/data/'

GALAXY_API_ROOT='api/<str:path>/'
