class Config:
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    ENVIRONMENT = "development"


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    ENVIRONMENT = "testing"


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}