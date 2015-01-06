DOCUMENT_TYPE = 'document'

DOCUMENT_MAPPING = {
    "_id": {
        "path": "id"
    },
    "_all": {
        "enabled": True
    },
    "dynamic": "strict",
    "properties": {
        "id": {"type": "string", "index": "not_analyzed"},
        "title": {"type": "string", "index": "analyzed"},
        "url": {"type": "string", "index": "not_analyzed"},
        "source_label": {"type": "string", "index": "not_analyzed"},
        "source_url": {"type": "string", "index": "not_analyzed"},
        "body": {"type": "string", "index": "analyzed"},
        # "created_at": {"type": "date", "index": "not_analyzed"},
        # "updated_at": {"type": "date", "index": "not_analyzed"},
        "entities": {
            "_id": {
                "path": "id"
            },
            "type": "nested",
            "include_in_parent": True,
            "properties": {
                "id": {"type": "string", "index": "not_analyzed"},
                "display_name": {"type": "string", "index": "not_analyzed"},
                "slug": {"type": "string", "index": "not_analyzed"}
            }
        }
    }
}

