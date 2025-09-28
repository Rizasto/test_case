import os
from configparser import ConfigParser
from pathlib import Path


def get_settings(config_uri, tag):
    config = ConfigParser()
    config.read(config_uri)
    return dict(config.items(tag))


PROJECT_DIRECTORY = Path(__file__).parent
CONFIG_PATH = PROJECT_DIRECTORY / 'settings.ini'


def get_setting_from_env(tp):
    if tp == 'db':
        if os.getenv('DB_USER'):
            return {
                'db_user': os.getenv('DB_USER'),
                'db_password': os.getenv('DB_PASSWORD'),
                'db_name': os.getenv('DB_NAME'),
                'db_host': os.getenv('DB_HOST'),
                'db_port': os.getenv('DB_PORT')
            }
        return get_settings(CONFIG_PATH, 'database')
    if tp == 'jwt':
        if os.getenv('AUTH_SECRET'):
            return {
                'auth_secret': os.getenv('AUTH_SECRET'),
                'access_ttl_min': os.getenv('ACCESS_TTL_MIN'),
                'algo': os.getenv('ALGO')
            }
        return get_settings(CONFIG_PATH, 'jwt')


DB_SETTINGS = get_setting_from_env('db')
JWT_SETTINGS = get_setting_from_env('jwt')
