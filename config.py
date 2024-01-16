"""
Class-based FastApi app Configuration.
config class is for base configuration.
"""
import os
from typing import List

from dotenv import load_dotenv, find_dotenv
from pydantic import Extra
from pydantic_settings import BaseSettings

SERVER_TYPE_PRODUCTION = "production"
SERVER_TYPE_DEVELOPMENT = "development"
load_dotenv(find_dotenv())


class TestConfig(BaseSettings):
    TEST_DB_URL: str

    class Config:
        extra = Extra.allow
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_TIME_MINUTES: int
    REFRESH_TOKEN_EXPIRE_TIME_HOURS: int

    JWT_ALGORITHM: str
    AUTH_JWT_HEADER_TYPE: str
    AUTH_SECRET_KEY: str
    # Configure algorithms which is permitted
    AUTH_JWT_DECODE_ALGORITHMS: List
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str


    class Config:
        extra = Extra.allow
        env_file = '.env'  # set the env file path.
        env_file_encoding = 'utf-8'


class JWTConfig(BaseSettings):
    # JWT Token configuration

    ACCESS_TOKEN_EXPIRE_TIME_MINUTES: int = Settings().ACCESS_TOKEN_EXPIRE_TIME_MINUTES
    REFRESH_TOKEN_EXPIRE_TIME_HOURS: int = Settings().REFRESH_TOKEN_EXPIRE_TIME_HOURS
    JWT_ALGORITHM: str = Settings().JWT_ALGORITHM
    AUTH_JWT_HEADER_TYPE: str = Settings().AUTH_JWT_HEADER_TYPE
    AUTH_SECRET_KEY: str = Settings().AUTH_SECRET_KEY
    # Configure algorithms which is permitted
    AUTH_JWT_DECODE_ALGORITHMS: List = Settings().AUTH_JWT_DECODE_ALGORITHMS
    authjwt_secret_key: str = Settings().AUTH_SECRET_KEY

class GoogleAuthConfig(BaseSettings):
    GOOGLE_CLIENT_ID: str = Settings().GOOGLE_CLIENT_ID
    GOOGLE_CLIENT_SECRET: str = Settings().GOOGLE_CLIENT_SECRET
    GOOGLE_REDIRECT_URI: str = Settings().GOOGLE_REDIRECT_URI
    


class DevelopmentConfig(object):
    """
        This class for generates the config for development instance.
    """
    DEBUG: bool = True
    TESTING: bool = False
    SQLALCHEMY_DATABASE_URL = Settings().SQLALCHEMY_DATABASE_URL


class ProductionConfig(object):
    """
    This class for generates the config for the development instance.
    """
    DEBUG: bool = False
    TESTING: bool = False


def get_current_server_config():
    """
    This will check FastApi_ENV variable and create an object of configuration according to that
    :return: Production or Development Config object.
    """
    current_config = os.getenv("ENV_FASTAPI_SERVER_TYPE", SERVER_TYPE_DEVELOPMENT)
    return DevelopmentConfig() if current_config == SERVER_TYPE_DEVELOPMENT else ProductionConfig()
