from os import environ

SETTING = environ.get('SETTING', None)
if SETTING is None or SETTING not in ('prod', 'dev'):
    raise ValueError('Set SETTING to prod or dev!')

if SETTING == 'prod':
    DATABASE_URL = environ.get('DATABASE_URL', None)
    if DATABASE_URL is None:
        raise ValueError(f'Set DATABASE_URL to correct value for prod environment!')
else:
    DATABASE_URL = environ.get('DEV_DATABASE_URL', None)
    if DATABASE_URL is None:
        raise ValueError(f'Set DEV_DATABASE_URL to correct value for dev environment!')

SECRET_KEY = environ.get('SECRET_KEY', None)
if SECRET_KEY is None:
    raise ValueError(f'Set SECRET_KEY value!')
