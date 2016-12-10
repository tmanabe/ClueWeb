import gzip
import re


class Collection(dict):  # is a dict where str (segment name) -> Segment
    def collect(self, document_ids, http=None, warc=None):
        d = {}
        result = []
        for document_id in sorted(document_ids):
            document_id = DocumentID(document_id)
            if document_id.segment not in d:
                d[document_id.segment] = []
            d[document_id.segment].append(document_id)
        for (s, document_ids) in d.items():
            result += self[s].collect(document_ids, http, warc)
        return result

    def get(self, document_id, default, http=None, warc=None):
        document_id = DocumentID(document_id)
        return self[document_id.segment].get(document_id, default, http, warc)

    def iterate(self, func, need_http=False, need_warc=False):
        for s in self.values():
            s.iterate(self, func, need_http, need_warc)

    def read(self, disk_path):
        raise NotImplementedError()


class Segment(list):  # is a list of Files
    def collect(self, document_ids, http=None, warc=None):
        d = {}
        result = []
        for document_id in sorted(document_ids):
            document_id = DocumentID(document_id)
            if document_id.file not in d:
                d[document_id.file] = []
            d[document_id.file].append(document_id)
        for (i, document_ids) in d.items():
            result += self[i].collect(document_ids, http, warc)
        return result

    def get(self, document_id, default, http=None, warc=None):
        document_id = DocumentID(document_id)
        return self[document_id.file].get(document_id, default, http, warc)

    def iterate(self, func, need_http=False, need_warc=False):
        for f in self:
            f.iterate(self, func, need_http, need_warc)

    def read(self, segment_path):
        raise NotImplementedError()


class File(str):  # is the path to a gzip file
    def __new__(self, path):
        self = str.__new__(self, path)
        return self

    def __init__(self, path):
        self.io = None

    def open(self):
        self.io = gzip.open(self)
        self.read_meta()

    def close(self):
        self.io.close()
        self.io = None

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
            if -1 < line.find(b'WARC/'):
                break
        self.line = line
        self.meta = meta

    def is_active(self):
        return self.line != b''

    def collect(self, document_ids, http=None, warc=None):
        self.open()
        result = []
        for target_id in sorted(document_ids):
            while(self.is_active()):
                w = {}
                self.read_warc(w)
                current_id = DocumentID(w[b'WARC-TREC-ID'].rstrip())
                if current_id == target_id:
                    if warc is not None:
                        warc.append(w)
                    if http is None:
                        self.read_http()
                    else:
                        h = {}
                        self.read_http(h)
                        http.append(h)
                    result.append(self.read_body())
                    self.read_tail()
                    break
                else:
                    self.read_http()
                    self.read_body()
                    self.read_tail()
        self.close()
        if len(result) < len(document_ids):
            raise IndexError('Some documents were not found.')
        else:
            return result

    def get(self, document_id, default, http=None, warc=None):
        try:
            return self.collect([document_id], http, warc)[0]
        except IndexError:
            if http is not None:
                http.append(default)
            if warc is not None:
                warc.append(default)
            return default

    def iterate(self, func, need_http=False, need_warc=False):
        self.open()
        while(self.is_active()):
            warc = {}
            self.read_warc(warc if need_warc else None)
            http = {}
            self.read_http(http if need_http else None)
            body = self.read_body()
            func(body, http, warc)
            self.read_tail()
        self.close()

    def read_warc(self, result=None):
        line = self.line
        if result is None:
            while(line.find(b'Content-Length: ')):
                line = self.io.readline()
            self.content_length = int(line.rsplit(b': ', 1)[-1])
            while(line.find(b'HTTP/')):
                line = self.io.readline()
        else:
            last_key = None
            while(line.find(b'HTTP/')):
                if(-1 < line.find(b': ')):
                    last_key, value = line.split(b': ', 1)
                    result[last_key] = value
                else:
                    result[last_key] = result.get(last_key, b'') + line
                line = self.io.readline()
            self.content_length = int(result[b'Content-Length'])
        self.line = line

    def read_http(self, result=None):
        line = self.line
        self.line = None
        length = self.content_length - len(line)
        if result is None:
            while(not re.match(b'\r?\n', line)):
                line = self.io.readline()
                length -= len(line)
        else:
            last_key = None
            while(not re.match(b'\r?\n', line)):
                if(-1 < line.find(b': ')):
                    last_key, value = line.split(b': ', 1)
                    result[last_key] = value
                else:
                    result[last_key] = result.get(last_key, b'') + line
                line = self.io.readline()
                length -= len(line)
        self.content_length = length

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
            self.io.close()
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
