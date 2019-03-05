import os


class Directories:
    def __init__(self):
        self.map = {}

    def create_directories(self, directory_dict: dict):
        for key, directory in directory_dict.items():
            self.create_directory(key, directory)

    def create_directory(self, key, directory):
        origin_directory_dict = self.map
        if key in origin_directory_dict:
            raise Exception('directory\'s key already exist')
        self.create_dir_if_not_exist(directory)
        origin_directory_dict.update({key: directory})

    def create_dir_if_not_exist(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def get_new_name_if_have_duplicate(self, path):
        origin_path = path
        suffix = 1
        have_duplicate = os.path.exists(path)
        while have_duplicate:
            suffix += 1
            path = origin_path + '_' + str(suffix)
            have_duplicate = os.path.exists(path)
        return path

    def remove_unused_directories_in_dict(self):
        removed_keys = []
        for key, path in self.map.items():
            if not os.listdir(path):
                os.removedirs(path)
                removed_keys.append(key)
        for key in removed_keys:
            del self.map[key]
