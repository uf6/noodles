# encoding: utf-8

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
from collections import defaultdict

from noodles import default_settings


norm_reqs = (
    ('limited liability partnership', 'llp'),
    ('limited liability company', 'llc'),
    ('public limited company', 'plc'),
    ('ltd\.?', 'limited'),
    ('b\.?v\.?', 'bv'),
    ('incorporated', 'inc'),
    ('inc\.', 'inc'),
    ('corporation', 'corp'),
    ('gesellschaft mit beschr[äa]nkter haftung', 'gmbh'),
    ('s.a.', 'sa'),
    #'SARL' => [/s\.?\s?[aà]\.? ?r\.?\s?l/i, /Soci[eé]t[eé] [aà] responsabilit[eé] limit[ée]e/i],
    #'SA' => [/s\.?a\.?/i, 'Sociedad An[oó]nima', 'Soci[eé]t[eé] Anonyme'],
    )



def eliminate_company_labels(coname):
    """
    Remove trailing company labels.
    Rule
    """
    company_eliminations = ('llp', 'llc', 'plc', 'limited', 'bv', 'gmbh', 'sa', 'inc')
    regex = re.compile('\W(' + '|'.join(company_eliminations) + ')\W?$')
    if len(coname.split(' ')) > 2:
        coname = regex.sub('', coname)
    return coname

def normalize(text):
    text = text.lower()
    for (rgx, replacement) in norm_reqs:
        text = re.sub(rgx, replacement, text)
    return text

class EntityExtractor(object):

    # ignore companies with names shorter than this
    # short names lead to many false positives
    MIN_TERM_LENGTH = 6

    # Should we remove Ltd, GmbH etc from company names before searching + indexing?
    # NB this will generate more matches, at the cost of more false positives
    STRIP_COMPANY_LABELS = True


    def __init__(self):
        escaped = map(re.escape, self.get_company_names())
        joined = '|'.join(escaped)
        self.regex = re.compile('(' + joined + ')')

    def get_company_names(self):
        datafiles = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/../data/*csv')
        names = set()
        for fn in datafiles:
            rows = csv.reader(open(fn, 'r'))
            rows.next() # skip header
            names.update(normalize(row[0]) for row in rows if len(normalize(row[0])) >= self.MIN_TERM_LENGTH)
        if self.STRIP_COMPANY_LABELS:
            names = set(eliminate_company_labels(x) for x in names)
        return names
        
    def es_entities(self, text):
        raw = self.entities_from_text(text)
        found = defaultdict(int)
        for name in raw:
            found[name] += 1
        output = []
        for entity_name, freq in found.items():
            output.append({
                'display_name': entity_name,
                'slug': entity_name,
                'mentions': freq,
            })
        return(output)


    def entities_from_text(self, text):
        return self.regex.findall(normalize(text))

