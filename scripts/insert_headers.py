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
from tqdm import tqdm
import re
import warnings
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from supermongo import headers_collection

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)

    dbdocuments = [{'path': fitsfile} for fitsfile in arguments['<fitsfile>']]

    for doc in tqdm(dbdocuments):
        doc['_id'] = '/'.join(doc['path'].split('/')[-3:])

        header = fits.getheader(doc['path'])
        header = dict(header)
        # _HeaderCommentaryCards objects need to be removed
        if 'COMMENT' in header.keys():
            del header['COMMENT']
        if 'HISTORY' in header.keys():
            del header['HISTORY']
        doc['header'] = header

        timestamp = datetime.strptime(header['DATE'], "%Y-%m-%dT%H:%M:%S")
        timestamp = timestamp.replace(tzinfo=ZoneInfo("UTC"))
        doc['timestamp'] = timestamp

        local_dt = timestamp.astimezone(ZoneInfo('America/Denver'))
        doc['date'] = (local_dt - timedelta(hours=12)).strftime("%Y-%m-%d")

        # add exposure numbers
        expnum_p = re.compile(r'\S*/\S*_([0-9]+)_\S*.fits')
        match = expnum_p.match(doc['path'])
        if match:
            doc['exposure_number'] = int(match.group(1))
        else:
            warnings.warning(f"unable to determine exposure number for raw frame {doc['path']}")

        if header['IMAGETYP'] == 'flat':
            doc['flat_time'] = 'morning' if local_dt.hour < 12 else 'evening'

    try:
        headers_collection.insert_many(dbdocuments)
    except Exception as e:
        print(repr(e), file=sys.stderr)
