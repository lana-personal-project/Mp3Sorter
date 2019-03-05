from audio_sorter.sorters.mp3Sorter import Mp3Sorter
import os


class Mp3CenterBitrateSorter(Mp3Sorter):
    def __init__(self):
        Mp3Sorter.__init__(self)
        self._center_bitrate = 320
        self._bitrate_list = [320]
        self._default_directories = {'higher': 'higherKbps', 'lower': 'lowerKbps', 'non_mp3': 'nonMp3'}

    def setup(self):
        self._setup_center_bitrate_from_input()
        self._overwrite_bitrate_list()
        super(Mp3CenterBitrateSorter, self).setup()

    def _setup_center_bitrate_from_input(self):
        bitrate = input('bitrate (default 320): ')
        try:
            self._center_bitrate = int(bitrate)
            print('-> bitrate: ' + str(self._center_bitrate))
        except ValueError:
            print('-> bitrate: ' + str(self._center_bitrate) + ' (default)')

    def _overwrite_bitrate_list(self):
        self._bitrate_list = [self._center_bitrate]

    def _get_sorted_part_by_bitrate(self, bitrate_by_kbps, file_name):
        if bitrate_by_kbps < self._center_bitrate:
            return os.path.join(self._directories.map['lower'], file_name)
        if bitrate_by_kbps > self._center_bitrate:
            return os.path.join(self._directories.map['higher'], file_name)
        if bitrate_by_kbps == self._center_bitrate:
            return os.path.join(self._directories.map[str(self._center_bitrate)], file_name)
