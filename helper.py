#!/usr/bin/env python
# coding: utf-8

import ClueWeb
import json
import sys


_, file_path, document_id = sys.argv
CODEC = ['utf-8', 'replace']
result, http, warc = {}, [], []
f = ClueWeb.File(file_path)
try:
    result['body'] = f.get(document_id, None, http, warc).decode(*CODEC)
except Exception:
    result['body'] = None
if result['body'] is not None:
    http, warc = http[0], warc[0]
    h = result['http'] = {}
    if b'Content-Type' in http:
        h['Content-Type'] = http[b'Content-Type'].decode(*CODEC).strip()
    else:
        h['Content-Type'] = 'text/html'
    if b'Date' in http:
        h['Date'] = http[b'Date'].decode(*CODEC).strip()
    else:
        h['Date'] = 'Thu, 10 May 2012 23:59:59 GMT'
    w = result['warc'] = {}
    w['WARC-Target-URI'] = warc[b'WARC-Target-URI'].decode(*CODEC)
print(json.dumps(result))
