"""
Find all company names in a piece of text

extractor = EntityExtractor()
entities = extractor.entities_from_text(text)
> ['acme incorporated', 'fubar limited', ...]
"""

import re
import csv
import string
import os
import glob


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
    datafiles = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/../data/*csv')
    names = set()
    for fn in datafiles:
        rows = csv.reader(open(fn, 'r'))
        names.update(normalize(row[0]) for row in rows)
    return names

def prepare_for_elasticsearch(entity_name):
    """
    Turn company name into an ickle bit of json, ready to be inserted
    into the json repository
    """
    return {
        'display_name': entity_name,
        'slug': entity_name}

class EntityExtractor(object):
    MIN_TERM_LENGTH = 6

    def __init__(self):
        self.company_names = [x for x in get_company_names() if len(x) >= self.MIN_TERM_LENGTH]
        normed = [re.escape(normalize(x)) for x in self.company_names]
        joined = '|'.join(normed)
        self.regex = re.compile('(' + joined + ')')

    def entities_from_text(self, text):
        return self.regex.findall(normalize(text))

