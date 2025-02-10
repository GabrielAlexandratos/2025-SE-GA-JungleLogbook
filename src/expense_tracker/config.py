import logging

class Config:
    LOG_LEVEL = logging.WARN
    LOG_FILENAME = 'app.log'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class DevelopmentConfig(Config):
    LOG_LEVEL = logging.INFO
    DEBUG = True
    ENVIRONMENT = "development"


class TestingConfig(Config):
    LOG_LEVEL = logging.INFO
    DEBUG = True
    TESTING = True
    ENVIRONMENT = "testing"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}