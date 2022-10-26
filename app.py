import helpers
from flask import Flask, render_template, redirect, url_for, request
import boto3
from werkzeug.utils import secure_filename

"""
import key_config as keys
s3 = boto3.client('s3',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN
                     )
"""

keys = helpers.get_aws_config()
s3 = boto3.client('s3',
                  aws_access_key_id=keys[0],
                  aws_secret_access_key=keys[1],
                  )

BUCKET_NAME = 'galleryeteenpain'


app = Flask(__name__)

images = ["/static/viiri.jpg"]


@app.route('/')
def kick_off():
    pic = images[0]
    return render_template("base.html", url=pic)


@app.route('/pelaajat', methods=['GET'])
def get_players():
    data_in = helpers.read_pickled()
    return render_template("/public/templates/pelaajat.html", details=data_in)


@app.get('/admin')
def player_home():
    data_in = helpers.read_pickled()
    return render_template("/admin/templates/admin_html.html", details=data_in)


@app.post("/admin/add")
def add_player():
    title = request.form.get("title")
    description = request.form.get("description")
    data = helpers.read_pickled()
    # estää "tyhjän" nimen talletuksen
    if len(title) > 0:  # title not in data and. Sallii vanhan nimen paivittamisen
        data[title] = description
        helpers.save_pickled(data)

    return redirect(url_for("player_home"))


# Ei kaytossa koska uuden pelaajan lisays toimii myos paivittamiseen
@app.get("/admin/update/<name>")
def update(name):
    description = request.form.get("description")
    data = helpers.read_pickled()
    data[name] = description
    helpers.save_pickled(data)
    return redirect(url_for("player_home"))


@app.get("/admin/delete/<name>")
def delete(name):
    data = helpers.read_pickled()
    data.pop(name)
    helpers.save_pickled(data)
    return redirect(url_for("player_home"))


@app.route('/tapahtumat')
def tapahtumat_home():
    """ should the pics be downloaded by default here or from the media folders???
        No, iterate over all the items in BUCKETNAME and print them as a media list on the left side of the page
        Then by clicking one of them download all the pics in that folder.
        Maybe first pic could be loaded by default to the list?
        @app.get("/tapahtumat/<name>", methods=['get'])
        def get_media(name)
    """
    folders = dict()
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Delimiter="/")
    response = response['CommonPrefixes']
    for item in response:
        folders[item['Prefix'][:-1]] = 0  # return the "folders"
    return render_template("/public/templates/tapahtumat.html", message=folders)


# write this to return objects from AWS s3 "folder"
# @app.get("/tapahtumat/<folder>", methods=['get'])
#def get_media(folder):
#    res = s3.download_file("sample-data", "a/foo.txt", "foo.txt")
#    return 1


@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            # get target folder as input. Below replace "Malaga_2022/" with the folder
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key='Malaga_2022/' + filename
                )
            msg = "Kuva talletettu! "

    return render_template("/public/templates/tapahtumat.html", msg=msg)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')


"""
Notes / code blocks / links
# check; https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/ for dockerizing and sql + media

@app.route("/")
def index():
    url = random.choice(images)
    return render_template("index.html", url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
    
# Testing different ways of sending dict()
@app.route('/<name>')
def user(name):
    # return f'Terve {name}' 
    dict_data = dict()
    url_sequence = 'data'
    dict_data[url_sequence] = helpers.read_pickled()
    return render_template('admin/templates/admin_html.html', web_data=dict_data, url_sequence=url_sequence)

"""