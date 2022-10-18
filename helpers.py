import pickle as pkl


@staticmethod
def read_pickled():
    return pkl.load(open('player_details.p', 'rb'))


@staticmethod
def save_pickled(data):
    pkl.dump(data, open('player_details.p', 'wb'))
