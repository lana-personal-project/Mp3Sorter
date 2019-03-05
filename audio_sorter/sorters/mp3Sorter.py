from audio_sorter.sorters.sorter import AbstractSorter


class Mp3Sorter(AbstractSorter):

    def __init__

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
        self.directories.remove_unnecessary_directories()
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
                sort_directory_path_dict = self.directories.directory_dict
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
