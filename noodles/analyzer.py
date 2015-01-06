from noodles.util import read_document, list_documents, write_document
from noodles.util import EXTRACTED_STAGE, ANALYZED_STAGE
from noodles import entities

extractor = entities.EntityExtractor()

def analyze_document(source, document_id):
    data = read_document(source, EXTRACTED_STAGE, document_id)
    data['entities'] = extractor.es_entities(data['text'])
    write_document(source, ANALYZED_STAGE, document_id, data)


def analyze_documents(source):
    for document_id in list_documents(source, EXTRACTED_STAGE):
        analyze_document(source, document_id)
        



