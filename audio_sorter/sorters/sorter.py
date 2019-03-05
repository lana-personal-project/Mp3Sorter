import os
from abc import ABC, abstractmethod
from multiprocessing.dummy import Pool
import multiprocessing
from audio_sorter.directories import Directories

import mutagen


class AbstractSorter(ABC):
    def __init__(self):
        self._source_directory = ''
        self._destination_directory = ''
        self._directories = Directories()
        self._audio = mutagen
        self._thread_pool = Pool()

    def setup(self):
        self._setup_thread_pool()
        self._setup_source_directory_from_input()
        self._setup_destination_directory()
        self._setup_directories()

    def _setup_thread_pool(self):
        max_thread = multiprocessing.cpu_count()
        threads_for_running = max_thread - 1
        self._thread_pool = Pool(threads_for_running)

    def _setup_source_directory_from_input(self):
        source = input('source directory path: ')
        if not os.path.exists(source):
            self._setup_source_directory_from_input()
        self._source_directory = source

    def _get_all_file_in_source(self):
        file_list = []
        for root, directories, files in os.walk(self._source_directory):
            for file in files:
                full_file_path = os.path.join(root, file)
                file_list.append(full_file_path)
        return file_list

    @abstractmethod
    def _setup_destination_directory(self):
        pass

    @abstractmethod
    def _setup_directories(self):
        pass
        self.sort()

    @abstractmethod
    def sort(self):
        pass
