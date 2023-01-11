import os
import pickle as pkl


def read_pickled():
    return pkl.load(open('player_details.p', 'rb'))


def save_pickled(data):
    pkl.dump(data, open('player_details.p', 'wb'))


def get_directories():

    # get list of directories
    data = os.listdir("static\pics")

    dirs = list()
    for item in data:
        if item.find('.') < 0:
            dirs.append(item)

    if dirs:
        return dirs
    else:
        print('No directories found')


def create_new_directory(folder):

    # Create the directory
    cur_dir = os.getcwd()
    path = os.path.join(cur_dir + "\\static\\pics\\", folder)

    # Create the directory
    try:
        os.makedirs(path)
        print("Directory '%s' created" % folder)
    except OSError as error:
        print(error)


def check_existence(folder):
    cur_dir = os.getcwd()
    path = os.path.join(cur_dir + "\\static\\pics\\", folder)
    return os.path.exists(path)


def get_images(image_folder):
    fin_folder = "static\pics\\" + image_folder
    images = ["/static/pics/" + image_folder + "/" + img for img in os.listdir(fin_folder)
              if img.endswith(".jpg") or
              img.endswith(".jpeg") or
              img.endswith("png") or
              img.endswith("PNG")]
    return images
