import os
from configparser import RawConfigParser
from pathlib import Path
from typing import List


def singleton(cls):
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance()


def parse_boolean_string(item: str) -> bool:
    item = item.rstrip().lstrip().lower()
    mapper = {'false': False, 'true': True}
    return mapper.get(item, False)


def parse_allowed_hosts(item: str) -> List[str]:
    items = item.strip().split('\n')
    return items


@singleton
class Configuration:

    def __init__(self):
        self._source = Path(os.path.dirname(__file__))
        self._conf = self._source.joinpath('conf')
        self._configurations = self._conf.joinpath('protrend_production.conf')

        config = RawConfigParser()
        config.read(self._configurations)

        self._db_user_name = str(config.get('protrend-db', 'user_name'))
        self._db_password = str(config.get('protrend-db', 'password'))
        self._db_ip = str(config.get('protrend-db', 'ip'))
        self._db_port = str(config.get('protrend-db', 'port'))

        self._secret_key = str(config.get('django-configuration', 'secret_key'))
        self._debug = parse_boolean_string(str(config.get('django-configuration', 'debug')))
        self._allowed_hosts = parse_allowed_hosts(config.get('django-configuration', 'allowed_hosts'))

        self._community_db_engine = str(config.get('protrend-community', 'db_engine'))
        self._community_db_name = str(config.get('protrend-community', 'db_name'))
        self._community_db_user = str(config.get('protrend-community', 'user_name'))
        self._community_db_password = str(config.get('protrend-community', 'password'))
        self._community_db_ip = str(config.get('protrend-community', 'ip'))
        self._community_db_port = str(config.get('protrend-community', 'port'))

        self._email_backend = str(config.get('protrend-email-configuration', 'email'))
        self._email_host = str(config.get('protrend-email-configuration', 'host'))
        self._email_port = str(config.get('protrend-email-configuration', 'port'))
        self._email_host_user = str(config.get('protrend-email-configuration', 'host_user'))
        self._email_host_password = str(config.get('protrend-email-configuration', 'host_password'))
        self._email_use_tls = parse_boolean_string(str(config.get('protrend-email-configuration', 'use_tls')))
        self._email_default = str(config.get('protrend-email-configuration', 'default_from_email'))
        self._email_verification = str(config.get('protrend-email-configuration', 'email_verification'))

        self._search_index = str(config.get('search-configuration', 'search_index'))

    @property
    def source(self):
        return self._source

    @property
    def conf(self):
        return self._conf

    @property
    def configurations(self):
        return self._configurations

    @property
    def db_user_name(self):
        return self._db_user_name

    @property
    def db_password(self):
        return self._db_password

    @property
    def db_ip(self):
        return self._db_ip

    @property
    def db_port(self):
        return self._db_port

    @property
    def bolt_url(self) -> str:
        return f'bolt://{self.db_user_name}:{self.db_password}@{self.db_ip}:{self.db_port}'

    @property
    def secret_key(self) -> str:
        return self._secret_key

    @property
    def debug(self) -> bool:
        return self._debug

    @property
    def allowed_hosts(self) -> List[str]:
        return self._allowed_hosts

    @property
    def community_db_engine(self):
        return self._community_db_engine

    @property
    def community_db_name(self):
        return self._community_db_name

    @property
    def community_db_user(self):
        return self._community_db_user

    @property
    def community_db_password(self):
        return self._community_db_password

    @property
    def community_db_ip(self):
        return self._community_db_ip

    @property
    def community_db_port(self):
        return self._community_db_port

    @property
    def email_backend(self):
        return self._email_backend

    @property
    def email_host(self):
        return self._email_host

    @property
    def email_port(self):
        return self._email_port

    @property
    def email_host_user(self):
        return self._email_host_user

    @property
    def email_host_password(self):
        return self._email_host_password

    @property
    def email_use_tls(self):
        return self._email_use_tls

    @property
    def email_default(self):
        return self._email_default

    @property
    def email_verification(self):
        return self._email_verification

    @property
    def search_index(self):
        return self._search_index


Configuration: Configuration
