from audio_sorter.sorters.sorter import AbstractSorter
import os
import shutil


class Mp3Sorter(AbstractSorter):

    def __init__(self):
        AbstractSorter.__init__(self)
        self.TYPE = 'mp3'
        self._bitrate_list = [128, 256, 320]
        self._default_directories = {'exception': 'unsorted', 'non_mp3': 'nonMp3', }

    def _setup_destination_directory(self):
        source = self._source_directory
        destination = source + '_sorted'
        self._destination_directory = self._directories.get_new_name_if_have_duplicate(destination)
        self._directories.create_dir_if_not_exist(self._destination_directory)

    def _setup_directories(self):
        self._insert_bitrate_directories_into_default_directories()
        self._directories.create_directories(self._get_full_path_default_directories())

    def _insert_bitrate_directories_into_default_directories(self):
        for bitrate in self._bitrate_list:
            self._default_directories.update({str(bitrate): str(bitrate) + 'kbps'})

    def _get_full_path_default_directories(self):
        directories_full_path = {}
        for key, directory in self._default_directories.items():
            directory = os.path.join(self._destination_directory, directory)
            directories_full_path.update({key: directory})
        return directories_full_path

    def sort(self):
        source_files = self._get_all_file_in_source()

        self._thread_pool.map(self._sort_one, source_files)
        self._thread_pool.close()
        self._thread_pool.join()
        self._directories.remove_unused_directories_in_dict()
        print('completed: ' + os.path.basename(self._destination_directory))

    def _sort_one(self, source_file):
        sorted_file = self._get_sorted_path(source_file)
        self._copy(source_file, sorted_file)

    def _get_sorted_path(self, source_file):
        audio = self._audio.File(source_file)
        file_name = os.path.basename(source_file)
        if audio is None:
            return None
        try:
            mp3 = self._audio.mp3.MP3(source_file)
            bitrate_by_kbps = round(mp3.info.bitrate / 1000)
            for bitrate in self._bitrate_list:
                if bitrate_by_kbps == bitrate:
                    return os.path.join(self._directories.map[str(bitrate)], file_name)

            file_name = str(bitrate_by_kbps) + '_' + file_name
            return os.path.join(self._directories.map['exception'], file_name)
        except self._audio.mp3.HeaderNotFoundError:
            return os.path.join(self._directories.map['non_mp3'], file_name)

    def _copy(self, src, dst):
        if dst is not None:
            file_name, extension = os.path.splitext(dst)
            suffix = 1
            while os.path.exists(dst):
                suffix += 1
                new_file_name = file_name + '_' + str(suffix)
                dst = new_file_name + extension
            shutil.copyfile(src, dst)
