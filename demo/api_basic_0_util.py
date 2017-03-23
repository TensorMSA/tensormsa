import os

def get_all_files(directory) :

    if not os.path.exists(directory):
        os.makedirs(directory)

    return_dict = {}
    count = 0
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            return_dict[''.join(['file', str(count)])] = open(filepath, 'rb')
            count = count + 1
    return return_dict