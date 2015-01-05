from noodles.util import read_document, list_documents
from noodles.util import ANALYZED_STAGE


def index_document(source, document_id):
    data = read_document(source, ANALYZED_STAGE, document_id)

    from pprint import pprint
    pprint(data)


def index_documents(source):
    for document_id in list_documents(source, ANALYZED_STAGE):
        index_document(source, document_id)


