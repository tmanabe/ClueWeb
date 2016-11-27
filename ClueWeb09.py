import ClueWeb
import os


class ClueWeb09(ClueWeb.Collection):
    def read(self, part_path):
        part_path = part_path.rstrip(os.sep)
        for segment_name in os.listdir(part_path):
            print(segment_name)
            segment_path = os.path.join(part_path, segment_name)
            self[segment_name] = Segment().read(segment_path)
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
