import ClueWeb
import os


class ClueWeb12(ClueWeb.Collection):
    def read(self, disk_path):
        disk_path = disk_path.rstrip(os.sep)
        for i in range(100):
            try:
                part_name = 'ClueWeb12_%s' % str(i).zfill(2)
                part_path = os.path.join(disk_path, part_name)
                for segment_name in os.listdir(part_path):
                    segment_path = os.path.join(part_path, segment_name)
                    self[segment_name] = Segment().read(segment_path)
            except FileNotFoundError:
                continue
        return self


class Segment(ClueWeb.Segment):
    def read(self, segment_path):
        segment_path = segment_path.rstrip(os.sep)
        segment_name = segment_path.rsplit(os.sep, 1)[-1]
        for i in range(100):
            try:
                file_name = '%s-%s.warc.gz' % (segment_name, str(i).zfill(2))
                file_path = os.path.join(segment_path, file_name)
                f = ClueWeb.File(file_path)
                self.append(f)
            except FileNotFoundError:
                break
        return self
