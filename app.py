import helpers
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# images = ["C://Users/akija/PycharmProjects/Flask/eteenpain/viiri2.jpg"]
images = ["/static/viiri.jpg"]


@app.route('/')
def kick_off():  # put application's code here
    pic = images[0]
    return render_template("base.html", url=pic)


@app.route('/<name>')
def user(name):
    # return f'Terve {name}'
    # taitais olla parempi tehdä jollain java scriptilla tai vastaavaa
    dict_data = dict()
    url_sequence = 'data'
    dict_data[url_sequence] = helpers.read_pickled()
    return render_template('admin/templates/admin_html.html', web_data=dict_data, url_sequence=url_sequence)


@app.route('/admin')
def admin():
    # add admin check here
    # pwd check to gt access to pickle file
    return redirect(url_for('user', name='Seniori'))


@app.route('/admin', methods=['GET'])
def get_players():
    web_indiv = {}
    url_sequence = 'test'
    web_indiv[url_sequence] = {'url': 'testabc', 'name': 'hello', 'count': 4}
    return render_template('admin_html.html', web_data=web_indiv, url_sequence=url_sequence)


# add logo. Need to a diff folder?
# check; https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/ for dockerizing and sql + media


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
# host="0.0.0.0" will make the page accessable by going to http://[ip]:5000/ on any computer in the network.
# app.run(host='0.0.0.0', port=80)


"""
@app.route("/")
def index():
    url = random.choice(images)
    return render_template("index.html", url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
"""