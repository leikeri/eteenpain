import helpers
from flask import Flask, render_template, redirect, url_for, request

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


# @app.route("pelaajat/add", methods=["POST"])
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