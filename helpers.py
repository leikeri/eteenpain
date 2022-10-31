import pickle as pkl


@staticmethod
def read_pickled():
    return pkl.load(open('player_details.p', 'rb'))


@staticmethod
def save_pickled(data):
    pkl.dump(data, open('player_details.p', 'wb'))


def get_aws_config():
    f = open("C://Users/akija/PycharmProjects/Flask/testuser_aws.txt") #  aws_settings.txt", "r")
    user = f.readline().rstrip("'\n").lstrip("USER: '")
    key = f.readline().lstrip("KEY: '")
    f.close()
    return user, key

