from noodles.sources.test import TestSource


SOURCES = {
    'test': TestSource
}


def extract(source):
    source = SOURCES[source](source)
    for document_id in source.extract():
        yield document_id
