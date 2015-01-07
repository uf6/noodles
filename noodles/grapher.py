import os
import logging
from hashlib import sha1
from itertools import combinations
import networkx as nx


from noodles.core import app
from noodles.util import read_document, list_documents
from noodles.util import ANALYZED_STAGE


log = logging.getLogger(__name__)


def graph_path():
    return os.path.join(app.config.get('DATA_PATH'), 'network.gexf')


def load_graph():
    if os.path.exists(graph_path()):
        return nx.read_gexf(graph_path())
    return nx.Graph()


def store_graph(g):
    return nx.write_gexf(g, graph_path())


def add_document(g, source, document_id):
    data = read_document(source, ANALYZED_STAGE, document_id)
    entities = set()
    log.info("Graphing %s", document_id)
    for entity in data.get('entities', []):
        id = sha1(entity.get('slug')).hexdigest()
        if not g.has_node(id):
            g.add_node(id, label=entity.get('display_name'))
        entities.add(id)

    for (a, b) in combinations(entities, 2):
        (a, b) = sorted((a, b))
        data = g.get_edge_data(a, b) or {'weight': 0}
        data['weight'] += 1
        if g.has_edge(a, b):
            g.remove_edge(a, b)
        g.add_edge(a, b, data)
        #print document_id, (a, b), 
    # data['entities'] = entities
    

def add_documents(source):
    g = load_graph()
    for document_id in list_documents(source, ANALYZED_STAGE):
        add_document(g, source, document_id)
    store_graph(g)
