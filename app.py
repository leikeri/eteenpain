import helpers as hp
from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
import os
from flask_login import LoginManager, login_required, current_user
from models import db, Users

from index import index
from login import login
from logout import logout
from register import register
from home import home

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Valvoja'  # 'secret_key_to_be_read_from_environment_variables_for_example'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../yonex.db'

login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
app.app_context().push()
login_manager.login_view = "login.show"

# app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(register)
app.register_blueprint(home)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


folders = dict()


@app.route('/')
def kick_off():
    return render_template("koti.html")


@app.route('/pelaajat', methods=['GET'])
def get_players():
    player_data = hp.read_pickled()
    return render_template("pelaajat.html", details=player_data)


@app.get('/admin')
def player_home():
    data_in = hp.read_pickled()
    return render_template("admin.html", details=data_in)


@app.post("/admin/add")
@login_required
def add_player():
    if current_user.id < 4:
        title = request.form.get("title")
        description = request.form.get("description")
        data = hp.read_pickled()
        # estää "tyhjän" nimen talletuksen
        if len(title) > 0:  # title not in data and. Sallii vanhan nimen paivittamisen
            data[title] = description
            hp.save_pickled(data)
        flash('Pelaaja lisätty')
        return redirect(url_for("player_home"))
    else:
        flash('Tarvitset ison Kukon oikeudet')
        return redirect(url_for("player_home"))


# Ei kaytossa koska uuden pelaajan lisays toimii myos paivittamiseen
@app.get("/admin/update/<name>")
@login_required
def update(name):
    if current_user.id < 4:
        description = request.form.get("description")
        data = hp.read_pickled()
        data[name] = description
        hp.save_pickled(data)
        return redirect(url_for("player_home"))
    else:
        flash('Tarvitset ison Kukon oikeudet')
        return redirect(url_for("player_home"))


@app.get("/admin/delete/<name>")
@login_required
def delete(name):
    if current_user.id < 4:
        data = hp.read_pickled()
        data.pop(name)
        hp.save_pickled(data)
        return redirect(url_for("player_home"))
    else:
        flash('Tarvitset ison Kukon oikeudet')
        return redirect(url_for("player_home"))


@app.route('/tapahtumat', methods=['GET'])
@login_required
def tapahtumat_home():
    folder_list = hp.get_directories()
    for item in folder_list:
        folders[item] = 0

    pics = hp.get_images('Malaga_2022')  # set to default when loaded first time
    return render_template("tapahtumat.html", message=folders, pic=pics)


@app.get("/tapahtumat/<folder>")
@login_required
def get_media(folder):
    album = hp.get_images(folder)
    return render_template("tapahtumat.html", message=folders, pic=album)


@app.route('/upload', methods=['post'])
@login_required
def upload():
    if request.method == 'POST':
        destination_folder = request.form.get('kohde_kansio')

        # jos kansiota ei ole olemassa, niin luo se
        if not hp.check_existence(destination_folder):
            hp.create_new_directory(destination_folder)

        # talleta
        app.config['UPLOAD_FOLDER'] = "static/pics/" + destination_folder
        file = request.files['file']
        filename = secure_filename(file.filename)
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except OSError as error:
            print('nimi on jo kansiossa')

        flash('Kuva talletettu!')
        return redirect(url_for("get_media", folder=destination_folder))


if __name__ == '__main__':
    app.debug = True
    # run first time to create the DB
    # from app import db
    # db.create_all()
    app.run(host='0.0.0.0')


"""
# images = ["/static/viiri.jpg"]
@app.route('/')
def kick_off():
    pic = images[0]
    return render_template("koti.html", url=pic)
"""
