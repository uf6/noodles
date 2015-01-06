import json
from os import path, makedirs, walk

from flask import Response, request

from noodles.core import app

EXTRACTED_STAGE = 'parsed'
ANALYZED_STAGE = 'analyzed'


def stage_path(source, stage):
    return path.join(app.config.get('DATA_PATH'), source, stage)


def document_path(source, stage, document_id):
    prefix = path.join(stage_path(source, stage), *document_id[:5])
    return path.join(prefix, document_id + '.json')


def read_document(source, stage, document_id):
    file_path = document_path(source, stage, document_id)
    if not path.isfile(file_path):
        return None
    try:
        with open(file_path, 'rb') as fh:
            return json.load(fh)
    except:
        return None


def has_document(source, stage, document_id):
    file_path = document_path(source, stage, document_id)
    return path.isfile(file_path)


def write_document(source, stage, document_id, data):
    file_path = document_path(source, stage, document_id)
    file_dir = path.dirname(file_path)
    try:
        makedirs(file_dir)
    except:
        pass
    with open(file_path, 'wb') as fh:
        json.dump(data, fh)


def list_documents(source, stage):
    for (dirpath, dirnames, filenames) in walk(stage_path(source, stage)):
        for filename in filenames:
            if filename.endswith('.json'):
                yield filename.replace('.json', '')


def jsonify(obj, status=200, headers=None):
    """ Custom JSONificaton to support obj.to_dict protocol. """
    data = json.dumps(obj)
    if 'callback' in request.args:
        cb = request.args.get('callback')
        data = '%s && %s(%s)' % (cb, cb, data)
    return Response(data, headers=headers,
                    status=status,
                    mimetype='application/json')
