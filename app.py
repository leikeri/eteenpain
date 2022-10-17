from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

images = ["C://Users/akija/PycharmProjects/Flask/eteenpain/viiri2.jpg"]
# images = ["viiri2.jpg"]

@app.route('/')
def hello_world():  # put application's code here
    pic = images[0]
    return render_template("base.html", url=pic)


@app.route('/<name>')
def user(name):
    return f'Terve {name}'


@app.route('/admin')
def admin():
    return redirect(url_for('user', name='Seniori'))

# how to publish this in html?
#    pic = images[0]
#    render_template("base.html", url=pic)

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