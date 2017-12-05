
class Config(object):
    """
    Common configurations
    """

    # Put any configurations here that are common across all environments

class StageConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False

app_config = {
    'stage': StageConfig,
    'production': ProductionConfig
}