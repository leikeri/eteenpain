import helpers
from flask import Flask, render_template, redirect, url_for, request
import boto3
from werkzeug.utils import secure_filename
import aws_auth_functions_2 as aws2
"""
import key_config as keys
s3 = boto3.client('s3',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    aws_session_token=keys.AWS_SESSION_TOKEN
                     )
"""

# keys = helpers.get_aws_config()
s3 = boto3.client('s3')
                  # aws_access_key_id=keys[0],
                  # aws_secret_access_key=keys[1],
                  # )

BUCKET_NAME = 'galleryeteenpain'


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
    """ should the pics be downloaded by default here or from the media folders???
        No, iterate over all the items in BUCKETNAME and print them as a media list on the left side of the page
    """
    folders = dict()
    # 1. authenticate  2. Get temp access token...
    # testing cognito funs
    # user_pool_id = "us-east-1:0719f112-2e98-47b2-b3e0-a7d285b26f2f"
    # client_id = "42op390n44fc9nsjbru7430t58"  # tama on eteenpain appin id numero
    # auth_tool = aws2.CognitoIdentityProviderWrapper(boto3.client('cognito-idp', 'us-east-1'), user_pool_id=user_pool_id, client_id=client_id)

    # to create a user. Send a confirmation code to the given email
    # read the username from the frontend
    # user = 'leikeri'
    # auth_tool.sign_up_user('testiuser', "Yonex1yonex!", 'aki.jarvenpaa@gmail.com')  # samaa emailia ei voi kaytta kuin kerran
    # read confirmation code from frontend, which user gets to hers/his email
    # confirm_code = '932927'  # mind " vs '
    # confirm = auth_tool.confirm_user_sign_up(user, confirmation_code=confirm_code)  # returns true if okay
    # to be continued

    # try:
    #    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Delimiter="/")
    #    response = response['CommonPrefixes']
    #    for item in response:
    #        folders[item['Prefix'][:-1]] = 0  # return the "folders"
    # except:
    folders['Malaga_2022'] = 0
    folders['Kimmo_mokki_2021'] = 0
    pic = images[1]
    # pic = 'https://galleryeteenpain.s3.us-east-1.amazonaws.com/Malaga_2022/malaga_ryhma.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEIr%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmV1LW5vcnRoLTEiRzBFAiEAs7dHrFGx3N4h1hOufEKMRbzTrzUJ8NJH5zSAeuWwnlcCIDAkbD%2BsfGbJCWJDMlpfbwKJjSHqUrZm%2FEVlqLtkCPXJKuQCCHMQABoMNTU5NTg4MzM3MzE4IgyqTUKyaoYCrO6%2FllsqwQKIjQxPzmOCnAwTsHXEErxlzkqk6VoG6J8Ip68z87sxl0Wn8woY4J1kymUiqdJvA48EnpWWvjDK9wYeQHV2%2FukjiMVuyAtp0rNi4EhD2pk8PBis0Hhlx1ewHFkis4aNQ8SXuosgIXcrQwL8byR2Ie737%2FMAg11aEyfyX91dT0wNUaQEIUMQcMlcDYzOoxK50QOjgJkvId3A1TjBrLD0ujSpRCXUUpa9%2BHc92EO2FUS%2BJ%2BKv%2BuUZpsMT8NbKo1XZhT8WzLnsTA2f0yF1v9axOfEl2UAvah44hvAZXo1p76sI4htEHkRd2bdeFDOC5irGrex610B0a71B5XmaeQnvhGbshiUoQ%2FkbNeVG3MIHf6BJ3XxyWAAX%2FYoKkFyM4%2B6VhoRt6h8icW98dM1MdSjto2v0c1ayfJr48L0qMPOHOS3WINUw3Jn%2BmgY6swIze0xlP0xuLIxmzQ3C8OS7DVwnUYDCMoTG8Hw7qZKtcARkwf3WXr6xS8uyHZNOZhW9NB%2Flqfh4L5fcMD%2FS8mMZhq88j%2B%2BETGTZsfDFLgpZiGjW%2Fn%2Fe2d8HYFVLFTI5swaGdq%2B4BPUkpvoiygiOzJHj832Ve4kpVVnjFK39KWBi3%2BJTwU630vIa1ypi9YpjjhudBr%2FyJk6xe9wZbmk7Faw3V%2FYhwfx%2B0ksntkmZ3IKHJaAw6JtbZih%2B1UOSJj3%2B%2BPbucy6CI3wNB2F2wjIHZg0hcyrGtg3zyueZedorrGsF5H0cO2j4IjIfWHdsmlniidLKDzUFGXd1mA%2BNian5qXaDwgk9JYRb14aL87pb7ruLCIYXHBxVlhv2YkEMNya6DxBF6aV4ftxATc4Ns0QUCcga5446&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20221031T131754Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIAYESQQM2TODRAWNXC%2F20221031%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=bcb5f0dc2c95408c40444eeb443b80708a1bb7511056740277f40d92ea43801a'
    return render_template("/public/templates/tapahtumat.html", message=folders, pic=pic)


# write this to return objects/links from AWS s3 "folder"
@app.get("/tapahtumat/<folder>")
def get_media(folder):
    # paras metodi? lataa kuvat joka kerta? Onko muita vaihtoehtoja. Ylla linkki, mutta sekin voimassa vaan maaritellyn ajan
    # res = s3.download_file("sample-data", "a/foo.txt", "foo.txt")
    return redirect(url_for("tapahtumat_home"))


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
                Key='Malaga_2022/' + filename  # replce hardcoded part to be read from html
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