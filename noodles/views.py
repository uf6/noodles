from flask import request

from noodles.core import app
from noodles.util import jsonify
from noodles import searcher


@app.route('/')
def index():
    return 'hello, world!'


@app.route('/api/suggest')
def suggest():
    prefix = request.args.get('prefix', '').lower()
    field = request.args.get('field', 'entities.suggest')
    res = searcher.suggest(field, prefix)
    return jsonify(res)
