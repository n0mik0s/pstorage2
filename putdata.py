import elasticsearch
import datetime
import elasticsearch.helpers

def _es_conn_ini(args):
    _return = False
    _args = args

    try:
        if _args['use_ssl']:
            _return = elasticsearch.Elasticsearch(
                _args['es_nodes'],
                port=_args['port'],
                http_auth=(_args['user'] + ':' + _args['password']),
                verify_certs=True,
                use_ssl=True,
                ca_certs=_args['ca_cert']
            )
        else:
            _return = elasticsearch.Elasticsearch(
                _args['es_nodes'],
                port=_args['port'],
                http_auth=(_args['user'] + ':' + _args['password'])
            )
    except Exception as _exc:
        print('ERR: [getdata:_es_conn_ini]: Error with establishing connection with elastic cluster:', _exc)
        return _return
    else:
        return _return

def elastic_bulk_insert(args, js_arr):
    _args = args
    _js_arr = js_arr
    _es_eng = _es_conn_ini(args=_args)
    _map = _args['mapping']
    _shards = _args['shards']
    _replicas = _args['replicas']
    _today = '{0:%Y-%m}'.format(datetime.datetime.today())
    _index = _args['pattern'] + _today

    _body = {
        "settings": {
            "number_of_shards": _shards,
            "number_of_replicas": _replicas
        },
        "mappings": _map["mappings"]
    }
    _actions = [
        {
            "_index": _index,
            "_source": _js
        }
        for _js in _js_arr
    ]
    if not _es_eng.indices.exists(index=_index):
        try:
            _es_eng.indices.create(index=_index, body=_body)
        except Exception as _err:
            print('ERR: [putdata:elastic_bulk_insert]', _err)
            return False
    try:
        elasticsearch.helpers.bulk(_es_eng, _actions, chunk_size=500, request_timeout=30)
    except Exception as _err:
        print('ERR: [putdata:elastic_bulk_insert]', _err)
        return False
    else:
        return True