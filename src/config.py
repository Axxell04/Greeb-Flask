import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    SECRET_KEY = os.getenv("SECRET_KEY")
    
class DevelopmentConfig(Config):
    DEBUG = True
    MAIN_PATH = os.path.dirname(os.path.abspath(__file__))
    STATIC_PATH = os.path.join(MAIN_PATH, "static")
    TEMPLATES_PAHT = os.path.join(MAIN_PATH, "templates")

class ProductionConfig(Config):
    DEBUG = False
    MAIN_PATH = os.path.dirname(os.path.abspath(__file__))
    STATIC_PATH = os.path.join(MAIN_PATH, "static")
    TEMPLATES_PAHT = os.path.join(MAIN_PATH, "templates")
    
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}