from pprint import pprint

from noodles.mapping import DOCUMENT_TYPE
from noodles.core import es, es_index


class ResultProxy(object):
    """ This is required for the pager to work. """

    def __init__(self, doc_type, query):
        self.doc_type = doc_type
        self.query = query
        self._result = None
        self._count = None
        self._limit = 10
        self._offset = 0

    def limit(self, num):
        self._result = None
        self._limit = num
        return self

    def offset(self, num):
        self._result = None
        self._offset = num
        return self

    @property
    def result(self):
        if self._result is None:
            q = self.query.copy()
            q['from'] = self._offset
            q['size'] = self._limit
            self._result = es.search(index=es_index,
                                     doc_type=self.doc_type,
                                     query=q)
            pprint(self._result)
        return self._result

    def __len__(self):
        if self._count is None:
            if self._result is None:
                #self.limit(0)
                res = self.result
                self._result = None
            else:
                res = self.result
            self._count = res.get('hits', {}).get('total')
        return self._count

    def __iter__(self):
        for hit in self.result.get('hits', {}).get('hits', []):
            res = hit.get('_source')
            res['score'] = hit.get('_score')
            yield res


def search(query):
    pprint(query)
    return ResultProxy(DOCUMENT_TYPE, query)


def suggest(field, prefix):
    query = {
        "suggest": {
            "text": prefix,
            "completion": {
                "field": field
            }
        }
    }
    res = es.send_request('POST', (es_index, '_suggest'), query)
    return res.get('suggest', {})[0]
