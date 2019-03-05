import shutil
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
        self._setup_directories()

    def _setup_thread_pool(self):
        max_thread = multiprocessing.cpu_count()
        threads_for_running = max_thread - 1
        self._thread_pool = Pool(threads_for_running)

    @abstractmethod
    def _setup_directories(self):
        pass
        self.sort()

    @abstractmethod
    def sort(self):
        pass
