"""
Find all company names in a piece of text

extractor = EntityExtractor()
entities = extractor.entities_from_text(text)
> ['acme incorporated', 'fubar limited', ...]
"""

COMPANY_SOURCE_FILE = '/tmp/companies_dev.csv'

import re
import csv

norm_reqs = (
    ('ltd.', 'limited'),
    (' bv ', 'b.v.'),
    )

def normalize(text):
    text = text.lower()
    for (rgx, replacement) in norm_reqs:
        text = re.sub(rgx, replacement, text)
    return text

def get_company_names():
    rows = csv.reader(open(COMPANY_SOURCE_FILE, 'r'))
    names = [normalize(row[0]) for row in rows]
    return names

class EntityExtractor(object):

    def __init__(self):
        normed = [re.escape(normalize(x)) for x in get_company_names()]
        joined = '|'.join(normed)
        self.regex = re.compile('(' + joined + ')')

    def entities_from_text(self, text):
        return self.regex.findall(normalize(text))

