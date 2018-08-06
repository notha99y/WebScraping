import os


def make_dir(directory):
    '''
    Creates a directory if there is no directory
    '''
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        print("Directory already exist: {}. No action taken".format(directory))


if __name__ == '__main__':
    pass
