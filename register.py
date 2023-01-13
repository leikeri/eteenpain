import sqlalchemy
from flask import Blueprint, url_for, render_template, redirect, request, flash
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from models import db, Users

register = Blueprint('register', __name__)  # , template_folder='../frontend')
login_manager = LoginManager()
login_manager.init_app(register)


@register.route('/register', methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if username and email and password and confirm_password:
            if password == confirm_password:
                hashed_password = generate_password_hash(password, method='sha256')
                try:
                    new_user = Users(username=username, email=email, password=hashed_password)
                    db.session.add(new_user)
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError:
                    flash('Käyttäjätunnus tai e-maili on jo käytössä')
                    return redirect(url_for('register.show') + '?error=user-or-email-exists')
                flash('Tilisi on luotu')
                return redirect(url_for('login.show') + '?success=account-created')
        else:
            flash('Tarkista kaikki kentät')
            return redirect(url_for('register.show') + '?error=missing-fields')
    else:
        return render_template('register.html')