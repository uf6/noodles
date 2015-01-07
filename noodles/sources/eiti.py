import logging
import urllib2
import csv
import os
import traceback

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter

from noodles.util import stage_path

from noodles.sources.common import Source

class EITISource(Source):

    LABEL = 'EITI Country Reports'
    URL = 'https://eiti.org/countries/reports'

    source_url = 'http://eiti.org/countries/reports/compare/download/csv'

    def _iterate_reports(self):
        csvfile = csv.DictReader(urllib2.urlopen(self.source_url), delimiter = ';')
        for line in csvfile:
            fn_to_store = 'eiti_%s_%s.pdf' % (line['Country Name'].strip(), line['Years Covered'])
            path = os.path.join(stage_path(self.name, 'download'), fn_to_store)
            url =  'https://eiti.org/files/%s' % line['EITI Report'].strip()
            if not os.path.exists(path):
                try:
                    os.makedirs(os.path.dirname(path))
                except:
                    pass
                with open(path, 'wb') as fh:
                    try:
                        fh.write(urllib2.urlopen(url).read())
                    except urllib2.URLError:
                        #traceback.print_exc()
                        continue
            text = self._txt_from_pdf(path)
            if text:
                yield text


    def _txt_from_pdf(self, pdf_fn):
        print(pdf_fn)
        return os.popen("pdftotext '%s' -" % pdf_fn).read()


    def extract(self):
        for report in self._iterate_reports():
            pass
