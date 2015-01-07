import logging
from hashlib import sha1
from pyelasticsearch.exceptions import IndexAlreadyExistsError

from noodles.core import collection
from noodles.mapping import DOCUMENT_MAPPING, DOCUMENT_TYPE
from noodles.util import read_document, list_documents
from noodles.util import ANALYZED_STAGE


log = logging.getLogger(__name__)


def load_document(source, document_id):
    data = read_document(source, ANALYZED_STAGE, document_id)
    data['id'] = document_id
    entities = []
    for entity in data.get('entities', []):
        entity['id'] = sha1(entity.get('slug')).hexdigest()
        entities.append(entity)
    data['entities'] = entities
    if entities:
        collection.insert(data)


def load_documents(source):
    for document_id in list_documents(source, ANALYZED_STAGE):
        load_document(source, document_id)
    #es.refresh(index=es_index)


def init():
    # es.delete_index(es_index)
    #try:
    #    es.create_index(es_index)
    #except IndexAlreadyExistsError:
    #    pass
    log.info("Creating MongoDB documents...")
    #data = {DOCUMENT_TYPE: DOCUMENT_MAPPING}
    #es.put_mapping(es_index, DOCUMENT_TYPE, data)
