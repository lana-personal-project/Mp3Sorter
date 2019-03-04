import os


class DirectoriesForSorter:
    def __init__(self):
        self.source_dir = ''
        self.destination_dir = ''
        self.exception_dir = ''
        self.unknown_dir = ''
        self.custom_dirs = {}

    def setup(self, directory_key_and_name_dict):
        self._get_and_setup_source_directory_from_input()
        self._setup_destination_directory()
        self._setup_directory_for_exception_and_unknown()
        self._setup_directory_for_sorting(directory_key_and_name_dict)

    def _get_and_setup_source_directory_from_input(self):
        is_work_dir_exist = False
        while not is_work_dir_exist:
            path = input('path to folder contains files: ')
            if os.path.exists(path):
                is_work_dir_exist = True
                self.source_dir = path
                print('-> working directory: ' + path)

    def _setup_destination_directory(self):
        destination_directory = self.source_dir + '_sorted'
        destination_directory = self._handle_duplicate(destination_directory)
        self.create_dir(destination_directory)
        self.destination_dir = destination_directory

    def _setup_directory_for_exception_and_unknown(self):
        self.unknown_dir = os.path.join(self.destination_dir, 'unknown')
        self.exception_dir = os.path.join(self.destination_dir, 'exception')
        self.create_dir(self.unknown_dir)
        self.create_dir(self.exception_dir)

    def _setup_directory_for_sorting(self, directory_names: dict):
        for key in directory_names.keys():
            directory = os.path.join(self.destination_dir, directory_names[key])
            if not os.path.exists(directory):
                self.create_dir(directory)
            directory_names[key] = directory
        self.custom_dirs = directory_names

    def create_dir(self, path):
        path = self._handle_duplicate(path)
        os.mkdir(path)

    def _handle_duplicate(self, path):
        origin_path = path
        suffix = 1
        have_duplicate = os.path.exists(path)
        while have_duplicate:
            suffix += 1
            path = origin_path + '_' + str(suffix)
            have_duplicate = os.path.exists(path)
        return path

    def remove_unnecessary_directories(self):
        self._remove_unused_custom_directories()
        if not os.listdir(self.exception_dir):
            os.removedirs(self.exception_dir)
        if not os.listdir(self.unknown_dir):
            os.removedirs(self.unknown_dir)

    def _remove_unused_custom_directories(self):
        for key, path in self.custom_dirs.items():
            if not os.listdir(path):
                os.removedirs(path)
