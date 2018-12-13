import gzip
import re


class Collection(dict):  # is a dict where str (segment name) -> Segment

    def collect(self, document_ids, https=None, warcs=None):
        buffer, results = {}, {}
        for document_id in sorted(set(document_ids)):
            document_id = DocumentID(document_id)
            if document_id.segment not in buffer:
                buffer[document_id.segment] = []
            buffer[document_id.segment].append(document_id)
        for (segment, document_ids) in buffer.items():
            results.update(self[segment].collect(document_ids, https, warcs))
        return results

    def get(self, document_id):
        document_id = DocumentID(document_id)
        return self[document_id.segment].get(document_id)

    def iterate(self, func, need_http=False, need_warc=False):
        for s in self.values():
            s.iterate(func, need_http, need_warc)

    def read(self, disk_path):
        raise NotImplementedError()


class Segment(list):  # is a list of Files

    def collect(self, document_ids, https=None, warcs=None):
        buffer, results = {}, {}
        for document_id in sorted(set(document_ids)):
            document_id = DocumentID(document_id)
            if document_id.file not in buffer:
                buffer[document_id.file] = []
            buffer[document_id.file].append(document_id)
        for (i, document_ids) in buffer.items():
            try:
                results.update(self[i].collect(document_ids, https, warcs))
            except Exception:
                import traceback
                print('Segment#collect: An error on ' + self[i])
                traceback.print_exc()
        return results

    def get(self, document_id):
        document_id = DocumentID(document_id)
        return self[document_id.file].get(document_id)

    def iterate(self, func, need_http=False, need_warc=False):
        for file in self:
            try:
                file.iterate(func, need_http, need_warc)
            except Exception:
                import traceback
                print('Segment#iterate: An error on ' + file)
                traceback.print_exc()

    def read(self, segment_path):
        raise NotImplementedError()


class File(str):  # is the path to a gzip file

    def __new__(self, path):
        self = str.__new__(self, path)
        return self

    def open(self):
        self.raw_io = open(self, 'rb', buffering=10**8)  # 100MB
        self.io = gzip.GzipFile(self, 'rb', fileobj=self.raw_io)
        self.read_meta()

    def close(self):
        self.io.close()
        self.raw_io.close()

    def read_meta(self):
        meta = {}
        line = self.io.readline()
        last_key = None
        while(True):
            if(-1 < line.find(b': ')):
                last_key, value = line.split(b': ', 1)
                meta[last_key] = value
            else:
                meta[last_key] = meta.get(last_key, b'') + line
            line = self.io.readline()
            if 0 == line.find(b'WARC/'):
                break
        self.line = line
        self.meta = meta

    def is_active(self):
        return self.line != b''

    def collect(self, document_ids, https=None, warcs=None):
        self.open()
        current_id, results = '(None)', {}
        for target_id in sorted(set(document_ids)):
            try:
                while(self.is_active()):
                    w = {}
                    self.read_warc(w)
                    current_id = DocumentID(w[b'WARC-TREC-ID'].rstrip())
                    if current_id == target_id:
                        if warcs is not None:
                            warcs[current_id] = w
                        if https is None:
                            self.read_http()
                        else:
                            h = {}
                            self.read_http(h)
                            https[current_id] = h
                        results[current_id] = self.read_body()
                        self.read_tail()
                        break
                    else:
                        self.read_http()
                        self.read_body()
                        self.read_tail()
            except Exception:
                import traceback
                print('File#collect: An error on ' + current_id)
                traceback.print_exc()
                break
        self.close()
        if len(results) < len(set(document_ids)):
            raise IndexError('Some documents were not found.')
        return results

    def get(self, document_id):
        h, w = {}, {}
        b = self.collect([document_id], h, w).get(document_id)
        return b, h.get(document_id), w.get(document_id)

    def iterate(self, func, need_http=False, need_warc=False):
        self.open()
        while(self.is_active()):
            warc = {} if need_warc else None
            self.read_warc(warc)
            http = {} if need_http else None
            self.read_http(http)
            body = self.read_body()
            func(body, http, warc)
            self.read_tail()
        self.close()

    def read_warc(self, results=None):
        line = self.line
        if results is None:
            while(line.find(b'Content-Length: ')):
                line = self.io.readline()
            self.content_length = int(line.rsplit(b': ', 1)[-1])
            while(not re.match(b'\r?\n', line)):
                line = self.io.readline()
        else:
            last_key = None
            while(not re.match(b'\r?\n', line)):
                if(-1 < line.find(b': ')):
                    last_key, value = line.split(b': ', 1)
                    results[last_key] = value
                else:
                    results[last_key] = results.get(last_key, b'') + line
                line = self.io.readline()
            self.content_length = int(results[b'Content-Length'])
        self.line = self.io.readline()  # Skip the empty line

    def read_http(self, results=None):
        line, length = self.line, self.content_length - len(self.line)
        last_key = None
        while(not re.match(b'\r*\n', line)):
            if results is not None:
                if(-1 < line.find(b': ')):
                    last_key, value = line.split(b': ', 1)
                    results[last_key] = value
                else:
                    results[last_key] = results.get(last_key, b'') + line
            line = self.io.readline()
            length -= len(line)
            if length < 0:
                self.io.seek(-len(line), 1)
                length += len(line)
                break
        self.line, self.content_length = None, length

    def read_body(self):
        length = self.content_length
        self.content_length = None
        return self.io.read(length)

    def read_tail(self):
        line = b'_'
        while(len(line) and line.find(b'WARC/')):
            line = self.io.readline()
        self.line = line

    def __del__(self):
        try:
            self.close()
        except AttributeError:
            pass


class DocumentID(str):
    def __new__(self, document_id):
        if isinstance(document_id, DocumentID):
            return document_id
        if isinstance(document_id, bytes):
            document_id = document_id.decode('utf-8')
        document_id = document_id.lower()
        tokens = document_id.split('-')
        if len(tokens) != 4:
            raise ValueError('Invalid document ID: %s' % document_id)
        self = str.__new__(self, document_id)
        self.collection = tokens[0]
        self.segment = tokens[1]
        self.file = int(tokens[2])
        self.document = int(tokens[3])
        return self
