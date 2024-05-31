import json
import os
import shutil
import sqlite3
from werkzeug.security import generate_password_hash
from entities import User, Project, Mail
from db import get_db
from config import config

class ModelUser():
    
    @classmethod
    def login(self, user: User):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user WHERE username = ?", (user.username,))
            res : sqlite3.Row = cursor.fetchone()
            if res:
                user = User(id=res["id_user"], username=res["username"], password=User.check_password(res["password"], user.password), admin=res["admin"])
                return user
            else:
                return None
    
    @classmethod
    def register(self, user: User, register_key: str):
        if register_key == os.getenv("REGISTER_KEY"):
            with get_db() as db:
                try:
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO user (username, password) VALUES (?, ?)", (user.username, generate_password_hash(user.password, salt_length=16)))
                    db.commit()
                    return True
                except sqlite3.IntegrityError:
                    return False
        else:
            return None
    
    @classmethod
    def get_by_id(self, id_user):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user WHERE id_user = ?", (id_user,))
            res : sqlite3.Row = cursor.fetchone()
            if res:
                return User(id=res["id_user"], username=res["username"], admin=res["admin"])
            else:
                return None

class ModelProject():
    
    @classmethod
    def get_all(self):
        with get_db() as db:
            list_projects = []
            cursor = db.cursor()
            cursor.execute("SELECT * FROM project")
            projects_res = cursor.fetchall()
            if projects_res:
                for project_row in projects_res:
                    images = []
                    cursor.execute("SELECT * FROM image WHERE id_project = ?", (project_row["id_project"],))
                    images_res = cursor.fetchall()
                    if images_res:
                        for image_row in images_res:
                            images.append(image_row["path"])
                    
                    project = Project(id=project_row["id_project"], name=project_row["name"], description=project_row["description"], site=project_row["site"], images=images)
                    list_projects.append(project)
            
            return list_projects
    
    @classmethod
    def get_last_project(self):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM project ORDER BY id_project DESC LIMIT 1")
            project_res = cursor.fetchone()
            if project_res:
                project = Project(id=project_res["id_project"], name=project_res["name"], description=project_res["description"], site=project_res["site"])
                return project
    
    @classmethod
    def add(self, project: Project):
        
        images_path = []
        images = project.get_images()
        
        STATIC_IMG_PATH = os.path.join(config["development"].STATIC_PATH, "img")

        if not os.path.exists(STATIC_IMG_PATH):
            os.mkdir(STATIC_IMG_PATH)

        if images:
            if not os.path.exists(os.path.join(STATIC_IMG_PATH, project.name)):
                os.mkdir(os.path.join(STATIC_IMG_PATH, project.name))
        for image in images:
            image_path = os.path.join("img", project.name, f"{images.index(image)}.{image.filename.split('.')[-1]}")
            image.save(os.path.join(config["development"].STATIC_PATH, image_path))
            images_path.append(image_path)
        
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO project (name, description, site) VALUES (?, ?, ?)", (project.name, project.description.strip(), project.site))
            cursor.lastrowid
            id_project = cursor.lastrowid
            for image_path in images_path:
                cursor.execute("INSERT INTO image (path, id_project) VALUES (?, ?)", (image_path, id_project))
                
            db.commit()

    @classmethod
    def delete(self, id=0):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM project WHERE id_project = ?", (id,))
            project_res = cursor.fetchone()
            if project_res:
                cursor.execute("DELETE FROM project WHERE id_project = ?", (id,))
                cursor.execute("DELETE FROM image WHERE id_project = ?", (id,))
                
                db.commit()

                STATIC_IMG_PATH = os.path.join(config["development"].STATIC_PATH, "img")
                if os.path.exists(os.path.join(STATIC_IMG_PATH, project_res["name"])):
                    shutil.rmtree(os.path.join(STATIC_IMG_PATH, project_res["name"]))

            


class ModelMessage():

    @classmethod
    def get_all(self):
        with get_db() as db:
            list_messages = []
            cursor = db.cursor()
            cursor.execute("SELECT * FROM message")
            messages_res = cursor.fetchall()
            if messages_res:
                for message_row in messages_res:
                    list_messages.append(Mail(id=message_row["id_message"], name=message_row["name"], email=message_row["email"], message=message_row["message"]))
            
            return list_messages

    @classmethod
    def get_last_message(self):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM message ORDER BY id_message DESC LIMIT 1")
            message_res = cursor.fetchone()
            if message_res:
                message = Mail(id=message_res["id_message"], name=message_res["name"], email=message_res["email"], message=message_res["message"])
                return message
    
    @classmethod
    def add(self, mail: Mail):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO message (name, email, message) VALUES (?, ?, ?)", (mail.name, mail.email, mail.message))

            db.commit()

                    
    
    
