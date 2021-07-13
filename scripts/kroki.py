# -*- coding:utf-8 -*-
import zlib
import base64
import sys

if __name__ == '__main__':
    complete_url = "".join(sys.argv[1:])
    url_apartments = complete_url.split("/")
    encode_diagram = url_apartments[-1]
    print(zlib.decompress(base64.urlsafe_b64decode(encode_diagram)).decode("utf-8"))