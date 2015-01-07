from hashlib import sha1

from noodles.util import write_document, has_document, EXTRACTED_STAGE


class Source(object):
    LABEL = None
    URL = None

    def __init__(self, name):
        self.name = name

    def extract(self):
        raise NotImplemented()

    def get_id(self, title=None, url=None, id=None):
        id = id or url or title
        return sha1(unicode(id).encode('utf-8')).hexdigest()

    def check(self, title=None, url=None, id=None):
        id = self.get_id(title=title, url=url, id=id)
        if has_document(self.name, EXTRACTED_STAGE, id):
            return id

    def emit(self, text=None, html=None, title=None, url=None, id=None):
        id = self.get_id(title=title, url=url, id=id)

        data = {
            'text': text,
            'html': html,
            'title': title,
            'url': url,
            'source_label': self.LABEL,
            'source_url': self.URL
        }
        #print data
        write_document(self.name, EXTRACTED_STAGE, id, data)
        return id
