import shutil
import os
from multiprocessing.dummy import Pool
import multiprocessing
from sorter.directories import DirectoriesForSorter as Directories

import mutagen


class Mp3Sorter:
    def __init__(self):

        self.TYPE = 'mp3'
        self.bitrate_list = [128, 320]
        self.directories = Directories()
        self.thread_pool = Pool()

    def setup(self):
        self._setup_thread_pool()
        self._setup_directory()

    def _setup_thread_pool(self):
        max_thread = multiprocessing.cpu_count()
        threads_for_running = max_thread - 1
        self.thread_pool = Pool(threads_for_running)

    def _setup_directory(self):
        bitrate_and_contained_directory_dict = {}
        for bitrate in self.bitrate_list:
            bitrate_and_contained_directory_dict.update({bitrate: str(bitrate)})
        self.directories.setup(bitrate_and_contained_directory_dict)

    def sort(self):
        source_directory = self.directories.source_dir
        source_files = self._get_source_file_path_list(source_directory)

        self.thread_pool.map(self._sort_one, source_files)
        self.thread_pool.close()
        self.thread_pool.join()
        print('completed: ' + os.path.basename(self.directories.destination_dir))

    def _get_source_file_path_list(self, path_to_folder):
        file_list = []
        for root, directories, files in os.walk(path_to_folder):
            for file in files:
                full_file_path = os.path.join(root, file)
                file_list.append(full_file_path)
        return file_list

    def _sort_one(self, source_file):
        sorted_file = self._get_sorted_path(source_file)
        self._copy(source_file, sorted_file)

    def _get_sorted_path(self, source_file):
        file = mutagen.File(source_file)
        file_name = os.path.basename(source_file)
        if file is None:
            return os.path.join(self.directories.unknown_dir, file_name)

        bitrate_by_kbps = round(file.info.bitrate / 1000)
        for bitrate in self.bitrate_list:
            if bitrate_by_kbps == bitrate:
                sort_directory_path_dict = self.directories.custom_dirs
                return os.path.join(sort_directory_path_dict[bitrate], file_name)

        file_name = str(bitrate_by_kbps) + '_' + file_name
        return os.path.join(self.directories.exception_dir, file_name)

    def _copy(self, src, dst):
        file_name, extension = os.path.splitext(dst)
        suffix = 1
        while os.path.exists(dst):
            suffix += 1
            new_file_name = file_name + '_' + str(suffix)
            dst = new_file_name + extension
        shutil.copyfile(src, dst)
