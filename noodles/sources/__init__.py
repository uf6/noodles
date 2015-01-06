from noodles.sources.test import TestSource
from noodles.sources.edgar import EdgarSource


SOURCES = {
    'test': TestSource,
    'edgar': EdgarSource
}


def extract(source):
    source = SOURCES[source](source)
    for document_id in source.extract():
        yield document_id
