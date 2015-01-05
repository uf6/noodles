from hashlib import sha1

from noodles.util import write_document, EXTRACTED_STAGE


class Source(object):
    LABEL = None
    URL = None

    def __init__(self, name):
        self.name = name

    def extract(self):
        raise NotImplemented()

    def emit(self, body=None, title=None, url=None, id=None):
        id = id or url or title
        id = sha1(unicode(id).encode('utf-8')).hexdigest()

        data = {
            'body': body,
            'title': title,
            'url': url,
            'source_label': self.LABEL,
            'source_url': self.URL
        }
        write_document(self.name, EXTRACTED_STAGE, id, data)
        return id
