#!/usr/bin/env python
# coding: utf-8

import ClueWeb
import json
import sys


_, file_path, document_id = sys.argv
result, http, warc = {}, [], []
f = ClueWeb.File(file_path)
try:
    result['body'] = f.get(document_id, None, http, warc).decode('utf-8')
except Exception:
    result['body'] = None
if result['body'] is not None:
    http, warc = http[0], warc[0]
    h = result['http'] = {}
    h['Content-Type'] = http[b'Content-Type'].decode('utf-8').strip()
    h['Date'] = http[b'Date'].decode('utf-8').strip()
    w = result['warc'] = {}
    w['WARC-Target-URI'] = warc[b'WARC-Target-URI'].decode('utf-8')
print(json.dumps(result))
