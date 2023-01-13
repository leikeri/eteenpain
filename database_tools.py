from app import db
from models import Users

db.create_all()


# delete records from a table
def delete_user(username):
    user_obj = Users.query.filter_by(username=username).first()
    try:
        db.session.delete(user_obj)
    except:
        print('Käyttäjätunnusta ei ole tietokannassa')
    db.session.commit()
    db.session.flush()


if __name__ == '__main__':

    name = 'Rooster'
    delete_user(name)
    users = Users.query.all()
    # print columns
    for user in users:
        print(user.username)
        # print(user.reg_date)
        print(f"<id={user.id}, username={user.username}>")
