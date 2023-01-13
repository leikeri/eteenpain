from flask import Blueprint, url_for, render_template, redirect, request, flash
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash
from models import Users

login = Blueprint('login', __name__)
login_manager = LoginManager()
login_manager.init_app(login)


@login.route('/login', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                # flash('Kukko, olet kirjautunut sisään!')
                return render_template('koti.html', user=username)  # redirect(url_for('kick_off', msg=username))
            else:
                flash('Salasana väärin. Yritä uudelleen')
                return redirect(url_for('login.show') + '?error=incorrect-password')
        else:
            flash('Käyttäjää ei löydy')
            return redirect(url_for('login.show') + '?error=user-not-found')
    else:
        return render_template('login.html')
