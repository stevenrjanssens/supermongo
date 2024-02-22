"""insert_headers.py -- insert headers into MongoDB

Usage:
    insert_headers.py [options] <fitsfile>...
    insert_headers.py -h | --help

Arguments:
    -h --help  Show this screen.
"""

import docopt
import sys
from astropy.io import fits
from pymongo import MongoClient

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)

    client = MongoClient('localhost', 27017)
    dbname = client['dfimages']
    collection_name = dbname['headers']

    for fitsfile in arguments['<fitsfile>']:
        header = fits.getheader(fitsfile)
        header = dict(header)

        # _HeaderCommentaryCards objects need to be removed
        if 'COMMENT' in header.keys():
            del header['COMMENT']
        if 'HISTORY' in header.keys():
            del header['HISTORY']

        try:
            collection_name.insert_one(header)
        except Exception as e:
            print(repr(e), file=sys.stderr)
            print(f'issue with {fitsfile}', file=sys.stderr)
