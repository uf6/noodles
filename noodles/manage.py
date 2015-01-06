import logging
from flask.ext.script import Manager
#from flask.ext.assets import ManageAssets

from noodles.views import app
from noodles.sources import SOURCES, extract as extract_
from noodles import analyzer, indexer


log = logging.getLogger(__name__)
manager = Manager(app)
# manager.add_command("assets", ManageAssets(assets))


@manager.command
def load(source=None):
    """ Extract, analyze and index all documents. If a source type is given,
    only documents from that source will be indexed. """
    indexer.init()
    sources = [source] if source else sorted(SOURCES.keys())
    for source in sources:
        for document_id in extract_(source):
            analyzer.analyze_document(source, document_id)
            indexer.index_document(source, document_id)


@manager.command
def extract(source=None):
    """ Extract all documents. If a source type is given, only documents
    from that source will be indexed. """
    sources = [source] if source else sorted(SOURCES.keys())
    for source in sources:
        for document_id in extract_(source):
            pass


@manager.command
def analyze(source=None):
    """ Analyze all documents. If a source type is given, only documents
    from that source will be indexed. """
    sources = [source] if source else sorted(SOURCES.keys())
    for source in sources:
        analyzer.analyze_documents(source)


@manager.command
def index(source=None):
    """ Index all documents. If a source type is given, only documents
    from that source will be indexed. """
    indexer.init()
    sources = [source] if source else sorted(SOURCES.keys())
    for source in sources:
        indexer.index_documents(source)


if __name__ == "__main__":
    manager.run()
