from app import db
from models import Users

db.create_all()

# Fetch all data to users
users = Users.query.all()
# print columns
for user in users:
    print(user.username)
    # print(user.reg_date)
    print(f"<id={user.id}, username={user.username}>")


# Inserts records into a mapping table
def insert_user(user_obj):
    db.session.add(user_obj)


# delete records from a table
def delete_user(username):
    user_obj = Users.query.filter_by(username=username).first()
    db.session.delete(user_obj)
    db.session.commit()
    db.session.flush()


if __name__ == '__main__':

    name = 'Laita kayttajanimi tahan'
    delete_user(name)
    users = Users.query.all()
    # print columns
    for user in users:
        print(user.username)
        # print(user.reg_date)
        print(f"<id={user.id}, username={user.username}>")

