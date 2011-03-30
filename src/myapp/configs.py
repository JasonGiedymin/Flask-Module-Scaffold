class Config(object):
    ## Base ##    
    DEBUG = False #Flask debug mode
    TESTING = False
    
    HOST = "127.0.0.1" #Flask host
    SERVER_NAME = "localhost"
    SERVER_PORT = "8080"
    
    SECRET_KEY = "That's what she said!"

    # Assets
    #ASSETS_DEBUG = False #Flask-Assets debug mode
    
    # DebugToolBar
    #DEBUG_TB_INTERCEPT_REDIRECTS = True
    
class ProductionConfig(Config):
    HOST = "0.0.0.0"
    SERVER_NAME = "example.com"
    SERVER_PORT = "80"

class DevelopmentConfig(Config):
    DEBUG = True
    SERVER_PORT = "8080"
    ASSETS_DEBUG = True

class TestinConfig(Config):
    TESTING = True
