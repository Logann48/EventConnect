class DevelopmentConfig():
    DEBUG=True
    
class Config:
    SECRET_KEY = 'clavesecreta123'

class DevelopmentConfig(Config):
    DEBUG= True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'eventconnect'

config={
    'development':DevelopmentConfig
    }