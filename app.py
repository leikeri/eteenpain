import helpers
from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)

images = ["/static/viiri.jpg", "/static/malaga_ryhma.jpg"]


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


@app.route('/tapahtumat', methods=['GET'])
def tapahtumat_home():
    """
        This function was intended to use aws services to register user and upload media files. Will be cleaned once
        final media storage provider found.
        should the pics be downloaded by default here or from the media folders???
        No, iterate over all the items in BUCKETNAME and print them as a media list on the left side of the page
    """
    folders = dict()
    folders['Malaga_2022'] = 0
    folders['Kimmo_mokki_2021'] = 0
    pic = images[1]
    return render_template("/public/templates/tapahtumat.html", message=folders, pic=pic)


# to be done for loading media. Content depend on the api/storage to be used
@app.get("/tapahtumat/<folder>")
def get_media(folder):
    # paras metodi? lataa kuvat joka kerta? Onko muita vaihtoehtoja.
    return redirect(url_for("tapahtumat_home"))


@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        # add content here for upload functionality
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