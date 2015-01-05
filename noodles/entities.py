"""
Find all company names in a piece of text

extractor = EntityExtractor()
entities = extractor.entities_from_text(text)
> ['acme incorporated', 'fubar limited', ...]

TODO:
 - work out a standard form to normalize company names to
 - import company names into the massive regex
"""


import re

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
    return ['ABC Inc', 'Joost Ltd.']

class EntityExtractor(object):

    def __init__(self):
        normed = [re.escape(normalize(x)) for x in get_company_names()]
        joined = '|'.join(normed)
        self.regex = re.compile('(' + joined + ')')

    def entities_from_text(self, text):
        return self.regex.findall(normalize(text))

