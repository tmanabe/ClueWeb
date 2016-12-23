import ClueWeb
from glob import glob
import os


class ClueWeb09(ClueWeb.Collection):
    def read(self, part_path):
        part_path = part_path.rstrip(os.sep)
        for segment_name in os.listdir(part_path):
            segment_path = os.path.join(part_path, segment_name)
            self[segment_name] = Segment().read(segment_path)
        return self

    def read_disk(self, disk_path):
        disk_path = disk_path.rstrip(os.sep)
        for part_path in glob(os.path.join(disk_path, 'ClueWeb09_*')):
            self.read(part_path)
        return self


class Segment(ClueWeb.Segment):
    def read(self, segment_path):
        segment_path = segment_path.rstrip(os.sep)
        for i in range(100):
            try:
                file_name = '%s.warc.gz' % (str(i).zfill(2))
                file_path = os.path.join(segment_path, file_name)
                f = ClueWeb.File(file_path)
                self.append(f)
            except FileNotFoundError:
                break
        return self
