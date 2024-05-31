from typing import Optional
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id=0, username="", password="", admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.admin = admin
    
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

class Project():
    def __init__(self, id=0, name="", description="", site="", images=[]):
        self.id = id
        self.name = name
        self.description = description
        self.site = site
        self.images = images
    
    # @classmethod
    def add_image(self, path):
        self.images.append(path)
    
    # @classmethod
    def get_images(self):
        return self.images


class Mail():
    def __init__(self, id=0, name="", email="", message=""):
        self.id = id
        self.name = name
        self.email = email
        self.message = message
