import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    SECRET_KEY = os.getenv("SECRET_KEY")
    MAIN_PATH = os.path.dirname(os.path.abspath(__file__))
    STATIC_PATH = os.path.join(MAIN_PATH, "static")
    IMG_PATH = os.path.join(STATIC_PATH, "img")
    TEMPLATES_PAHT = os.path.join(MAIN_PATH, "templates")
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

def init_directories():
    if not os.path.exists(Config.STATIC_PATH):
        os.mkdir(Config.STATIC_PATH)
        
    if not os.path.exists(Config.IMG_PATH):
        os.mkdir(Config.IMG_PATH)

init_directories()