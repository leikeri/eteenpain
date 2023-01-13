from flask import Blueprint, redirect, url_for

index = Blueprint('index', __name__)  # , template_folder='../frontend')


@index.route('/', methods=['GET'])
def show():
    return redirect('home')

