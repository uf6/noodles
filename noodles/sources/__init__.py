from noodles.sources.test import TestSource
from noodles.sources.edgar import EdgarSource
from noodles.sources.allafrica import AllAfricaSource


SOURCES = {
    'test': TestSource,
    'allafrica': AllAfricaSource,
    #'edgar': EdgarSource
}


def extract(source):
    source = SOURCES[source](source)
    for document_id in source.extract():
        yield document_id
