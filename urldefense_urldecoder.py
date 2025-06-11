#!/usr/bin/env python3
__author__ = 'Eric Van Cleve; Oleksandr Vlasiuk'
__license__ = 'GPL v.3'
__version__ = '4.0'
__email__ = 'oleksandr.vlasiuk@gmail.com'
__status__ = 'beta'


import sys
import re
from base64 import urlsafe_b64decode
# Uncomment for Python 2
# import string
# if sys.version_info[0] < 3:
#     from urllib import unquote
#     import HTMLParser
#     htmlparser = HTMLParser.HTMLParser()
#     unescape = htmlparser.unescape
#     from string import maketrans
# else:
from urllib.parse import unquote
from html import unescape
maketrans = str.maketrans


class URLDecoder:

    def __init__(self):
        URLDecoder.ud_pattern = re.compile(r'http.+?urldefense(?:\.proofpoint)?\.com/(v[0-9])/')
        URLDecoder.v1_pattern = re.compile(r'u=(?P<url>.+?)&k=')
        URLDecoder.v2_pattern = re.compile(r'http.+?urldefense\.proofpoint\.com/v2/url\?u=(?P<url>.+?)&[dc]=.*?&e=')
        URLDecoder.v3_pattern = re.compile(r'http.+?urldefense\.com/v3/__(?P<url>.+?)__;(?P<enc_bytes>.*?)!.*?\$')
        URLDecoder.v3_token_pattern = re.compile("\*(\*.)?")
        URLDecoder.v3_run_mapping = {'A': 2, 'B': 3, 'C': 4, 'D': 5, 'E':
                                            6, 'F': 7, 'G': 8, 'H': 9, 'I': 10,
                                            'J': 11, 'K': 12, 'L': 13, 'M': 14,
                                            'N': 15, 'O': 16, 'P': 17, 'Q': 18,
                                            'R': 19, 'S': 20, 'T': 21, 'U': 22,
                                            'V': 23, 'W': 24, 'X': 25, 'Y': 26,
                                            'Z': 27, 'a': 28, 'b': 29, 'c': 30,
                                            'd': 31, 'e': 32, 'f': 33, 'g': 34,
                                            'h': 35, 'i': 36, 'j': 37, 'k': 38,
                                            'l': 39, 'm': 40, 'n': 41, 'o': 42,
                                            'p': 43, 'q': 44, 'r': 45, 's': 46,
                                            't': 47, 'u': 48, 'v': 49, 'w': 50,
                                            'x': 51, 'y': 52, 'z': 53, '0': 54,
                                            '1': 55, '2': 56, '3': 57, '4': 58,
                                            '5': 59, '6': 60, '7': 61, '8': 62,
                                            '9': 63, '-': 64, '_': 65}
        URLDecoder.safelinks = re.compile(r'http.+?\.safelinks\.protection\.outlook\.com/\?url=(?P<url>.+?)&(?:amp;)?data=.*?reserved=0')

    def decode(self, line):
        match = self.ud_pattern.search(line)
        match_safelinks = self.safelinks.search(line)
        if match:
            if match.group(1) == 'v1':
                line =  self.v1_pattern.sub(self.unescquote, line)
            elif match.group(1) == 'v2':
                line = self.v2_pattern.sub(self.decode_v2, line)
            elif match.group(1) == 'v3':
                line = self.v3_pattern.sub(self.decode_v3, line)
        if match_safelinks:
            line = self.safelinks.sub(self.unescquote, line)
        return line

    def unescquote(self, match):
        return unescape(unquote(match.group('url')))

    def decode_v2(self, match):
        trans = maketrans('-_', '%/')
        url_encoded_url = match.group('url').translate(trans)
        return unescape(unquote(url_encoded_url))

    def decode_v3(self, match):
        def replace_token(token):
            if token == '*':
                character = self.dec_bytes[self.current_marker]
                self.current_marker += 1
                return character
            if token.startswith('**'):
                run_length = self.v3_run_mapping[token[-1]]//2
                run = self.dec_bytes[self.current_marker:self.current_marker+run_length]
                self.current_marker += run_length
                return run

        def substitute_tokens(text, start_pos=0):
            match = self.v3_token_pattern.search(text, start_pos)
            if match:
                start = text[start_pos:match.start()]
                built_string = start
                token = text[match.start():match.end()]
                built_string += replace_token(token)
                built_string += substitute_tokens(text, match.end())
                return built_string
            else:
                return text[start_pos:len(text)]

        url = match.group('url')
        encoded_url = unquote(url)
        enc_bytes = match.group('enc_bytes')
        enc_bytes += '=='
        self.dec_bytes = (urlsafe_b64decode(enc_bytes)).decode('utf-8')
        self.current_marker = 0
        return substitute_tokens(encoded_url)



def main():
    urldec = URLDecoder()
    for line in sys.stdin:
        sys.stdout.write(urldec.decode(line))
if __name__ == '__main__':
    main()
