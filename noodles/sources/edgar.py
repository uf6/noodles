import os
import ftplib
import logging
import urllib
from hashlib import sha1

from werkzeug.utils import secure_filename
from lxml import etree, html

from noodles.core import app
from noodles.util import stage_path
from noodles.sources.common import Source


log = logging.getLogger(__name__)

HOST = 'ftp.sec.gov'
BASE_DIR = 'edgar/monthly'
EDGNS = '{http://www.sec.gov/Archives/edgar}'
SICS = [1311, 1381, 1382, 1389, 2911, 2990, 3532,
        3533, 5171, 5172, 6792]


class EdgarSource(Source):

    LABEL = "SEC EDGAR"
    URL = "http://sec.gov"

    def monthly_indexes(self):
        ftp = ftplib.FTP(HOST)
        ftp.login('anonymous', '@anonymous')
        ftp.cwd(BASE_DIR)
        for file_name in ftp.nlst():
            path = os.path.join(stage_path(self.name, 'download'), file_name)
            if not os.path.exists(path):
                try:
                    os.makedirs(os.path.dirname(path))
                except:
                    pass
                with open(path, 'wb') as fh:
                    ftp.retrbinary("RETR " + file_name, fh.write)
            yield path
        ftp.quit()

    def parse_feed(self, file_name):
        doc = etree.parse(file_name)
        for item in doc.findall('.//item'):
            data = {}
            for c in item.iterchildren():
                if EDGNS in c.tag:
                    continue
                if c.tag == 'enclosure':
                    data[c.tag] = c.get('url')
                else:
                    data[c.tag] = c.text

            for fc in item.findall(EDGNS + 'xbrlFiling/*'):
                tag = fc.tag.replace(EDGNS, '')
                if tag == 'xbrlFiles':
                    continue

                if fc.text:
                    data[tag] = fc.text

            log.info('Filing title: %s', data.get('title'))

            if data.get('assignedSic') is None or \
                    int(data['assignedSic']) not in SICS:
                continue
            
            for fc in item.findall(EDGNS + 'xbrlFiling//' + EDGNS + 'xbrlFile'):
                file_data = data.copy()
                for k, v in fc.attrib.items():
                    file_data[k.replace(EDGNS, 'file_')] = v
                
                url = file_data.get('file_url', '')
                _, ext = os.path.splitext(url.lower())
                if ext in ['.htm', '.html', '.txt']:
                    html_text = self.download_filing(url)
                    doc = html.fromstring(html_text)
                    plain_text = doc.text_content()
                    yield {
                        'id': sha1(url).hexdigest(),
                        'url': url,
                        'title': file_data.get('title'),
                        'html': html_text,
                        'text': plain_text
                    }

    def download_filing(self, url):
        file_name = secure_filename(url)
        path = os.path.join(stage_path(self.name, 'filings'), file_name)
        if not os.path.exists(path):
            try:
                os.makedirs(os.path.dirname(path))
            except:
                pass
            urllib.urlretrieve(url, path)
        with open(path, 'rb') as fh:
            try:
                return fh.read().decode('utf-8')
            except:
                return fh.read().decode('ascii', 'ignore')

    def extract(self):
        for file_path in self.monthly_indexes():
            for filing in self.parse_feed(file_path):
                yield self.emit(**filing)
