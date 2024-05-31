from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from db import close_db, init_db
from models import ModelUser, ModelProject, ModelMessage
from entities import User, Project, Mail

from config import config

app = Flask(__name__)
app.config.from_object(config["development"])
app.teardown_appcontext(close_db)

with app.app_context():
    init_db(app)


login_manager_app = LoginManager()
login_manager_app.init_app(app)

crsf = CSRFProtect()
crsf.init_app(app)

@login_manager_app.user_loader  
def load_user(id_user):
    return ModelUser.get_by_id(id_user)
        

@app.route("/")
def inicio():
    return render_template("inicio.html")

@app.route("/proyectos")
def proyectos():
    projects = []
    with app.app_context():
        projects = ModelProject.get_all()
    return render_template("proyectos.html", projects=projects)

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        with app.app_context():
            try:
                email = request.form["email"]
                name = request.form["name"]
                message = request.form["message"]
                ModelMessage.add(Mail(name=name, email=email, message=message))

                flash("success")
                return redirect(url_for("contacto"))
            except:
                flash("error")
                return redirect(url_for("contacto"))

    return render_template("contacto.html")
        

## ADMIN ##

@app.route("/admin/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        with app.app_context():
            try:
                username = request.form["username"]
                password = request.form["password"]
                register_key = request.form["register_key"]
                user = ModelUser.register(User(username=username, password=password), register_key)
                if user:
                    flash("Usuario registrado con éxito")
                elif user == False:
                    flash(f"El usuario {username} ya existe")
                else:
                    flash("Llave de registro incorrecta")
            except Exception as e:
                flash("Error al registrar usuario")
            finally:
                return redirect(url_for("register"))
    
    return render_template("admin/register.html")

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        with app.app_context():
            try:
                username = request.form["username"]
                password = request.form["password"]
                user = ModelUser.login(User(username=username, password=password))
                if not user:
                    flash("Usuario no existe")
                elif user.password:
                    login_user(user)
                    return redirect(url_for("dashboard"))
                else:
                    flash("Contraseña incorrecta")
            except:
                flash("Error al iniciar sesión")

            return redirect(url_for("login"))
    
    return render_template("admin/login.html")

@app.route("/admin/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/admin/dashboard")
@login_required
def dashboard():
    last_project = None
    last_message = None
    with app.app_context():
        last_project = ModelProject.get_last_project()
        last_message = ModelMessage.get_last_message()
    return render_template("admin/dashboard.html", last_project=last_project, last_message=last_message)

@app.route("/admin/proyectos", methods=["GET", "POST", "DELETE"])
@login_required
def admin_proyectos():
    if request.method == "DELETE":
        with app.app_context():
            try:
                # id_project = request.form["id_project"]
                # ModelProject.delete(id_project)
                # flash(f"Proyecto {id_project} eliminado")
                flash(request.form)
            except Exception as e:
                # flash("Error al eliminar proyecto")
                flash(e)
            return redirect(url_for("admin_proyectos", _method="GET"))

    if request.method == "POST":
        with app.app_context():
            try:
                name = request.form["name"]
                description = request.form["description"]
                site = request.form.get("site", default=None)
                images = []
                if "image" in request.files:
                    for image in request.files.getlist("image"):
                        images.append(image)
                
                ModelProject.add(Project(name=name, description=description, site=site, images=images))
            except Exception as e:
                flash("Error al crear proyecto")
                # flash(str(e))

            return redirect(url_for("admin_proyectos"))
    projects = []
    with app.app_context():
        projects = ModelProject.get_all()
        
    return render_template("admin/proyectos.html", projects=projects)

@app.route("/admin/proyectos/eliminar/<int:id_project>")
@login_required
def admin_proyectos_eliminar(id_project):
    with app.app_context():
        ModelProject.delete(id_project)
    return redirect(url_for("admin_proyectos"))

@app.route("/admin/mensajes")
@login_required
def admin_mensajes():
    messages = []
    with app.app_context():
        messages = ModelMessage.get_all()
    
    return render_template("admin/mensajes.html", messages=messages)    


## Errors ##

def status_401(error):
    return redirect(url_for("login"))

def status_404(error):
    return redirect(url_for("inicio"))


app.register_error_handler(401, status_401)
app.register_error_handler(404, status_404)