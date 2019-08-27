import elasticsearch
import datetime
import elasticsearch.helpers
import statistics
import json

from queries import *

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

def cpu(args, node):
    _args = args
    _es_eng = _es_conn_ini(args=_args)
    _node = str(node)
    _query = q_cpu
    _scroll = str(_args['scroll'])
    _size = int(_args['size'])
    _index = _args['pattern']
    _cpu_dict = {'cpu_total': [],
                 'cpu_system': [],
                 'cpu_idle': [],
                 'cpu_user': []}
    _result = []
    _today = '{0:%Y-%m-%d}'.format(datetime.datetime.today())

    try:
        _query['query']['bool']['must'][2]['match']['host.name'] = _node
    except Exception as _err:
        print('ERR: [getdata:cpu]', _err)
        return False
    else:
        try:
            _scan_res = elasticsearch.helpers.scan(client=_es_eng,
                                                   request_timeout=30,
                                                   query=_query,
                                                   scroll=_scroll,
                                                   size=_size,
                                                   index=_index,
                                                   clear_scroll=True,
                                                   raise_on_error=False)
        except Exception as _err:
            print('ERR: [getdata:cpu]', _err)
            return False
        else:
            _scan_res = list(_scan_res)
            if len(_scan_res) > 0:
                for _hit in _scan_res:
                    _cpu_cores = _hit['_source']['system']['cpu']['cores']

                    _cpu_total = round(((_hit['_source']['system']['cpu']['total']['pct'] * 100) / _cpu_cores), 2)
                    _cpu_system = round(((_hit['_source']['system']['cpu']['system']['pct'] * 100) / _cpu_cores), 2)
                    _cpu_idle = round(((_hit['_source']['system']['cpu']['idle']['pct'] * 100) / _cpu_cores), 2)
                    _cpu_user = round(((_hit['_source']['system']['cpu']['user']['pct'] * 100) / _cpu_cores), 2)

                    _cpu_dict['cpu_total'].append(_cpu_total)
                    _cpu_dict['cpu_system'].append(_cpu_system)
                    _cpu_dict['cpu_idle'].append(_cpu_idle)
                    _cpu_dict['cpu_user'].append(_cpu_user)

                _result.append(json.dumps({'cpu_total': round((statistics.mean(_cpu_dict['cpu_total'])), 2),
                                            'cpu_system': round((statistics.mean(_cpu_dict['cpu_system'])), 2),
                                            'cpu_idle': round((statistics.mean(_cpu_dict['cpu_idle'])), 2),
                                            'cpu_user': round((statistics.mean(_cpu_dict['cpu_user'])), 2),
                                            "node": _node,
                                            "@timestamp": _today,
                                            "metricset_module": "system",
                                            "metricset_name": "cpu"}))

    return _result

def memory(args, node):
    _args = args
    _es_eng = _es_conn_ini(args=_args)
    _node = str(node)
    _query = q_memory
    _scroll = str(_args['scroll'])
    _size = int(_args['size'])
    _index = _args['pattern']
    _mem_dict = {'memory_actual_used': [],
                 'memory_swap_used': [],
                 'memory_used': []}
    _result = []
    _today = '{0:%Y-%m-%d}'.format(datetime.datetime.today())

    try:
        _query['query']['bool']['must'][2]['match']['host.name'] = _node
    except Exception as _err:
        print('ERR: [getdata:memory]', _err)
        return False
    else:
        try:
            _scan_res = elasticsearch.helpers.scan(client=_es_eng,
                                                   request_timeout=30,
                                                   query=_query,
                                                   scroll=_scroll,
                                                   size=_size,
                                                   index=_index,
                                                   clear_scroll=True,
                                                   raise_on_error=False)
        except Exception as _err:
            print('ERR: [getdata:memory]', _err)
            return False
        else:
            _scan_res = list(_scan_res)
            if len(_scan_res) > 0:
                for _hit in _scan_res:
                    _memory_actual_used = round((_hit['_source']['system']['memory']['actual']['used']['pct'] * 100), 2)
                    _memory_swap_used = round((_hit['_source']['system']['memory']['swap']['used']['pct'] * 100), 2)
                    _memory_used = round((_hit['_source']['system']['memory']['used']['pct'] * 100), 2)

                    _mem_dict['memory_actual_used'].append(_memory_actual_used)
                    _mem_dict['memory_swap_used'].append(_memory_swap_used)
                    _mem_dict['memory_used'].append(_memory_used)

                _result.append(
                    json.dumps({'memory_actual_used': round((statistics.mean(_mem_dict['memory_actual_used'])), 2),
                                'memory_swap_used': round((statistics.mean(_mem_dict['memory_swap_used'])), 2),
                                'memory_used': round((statistics.mean(_mem_dict['memory_used'])), 2),
                                "node": _node,
                                "metricset_module": "system",
                                "@timestamp": _today,
                                "metricset_name": "memory"}))

        return _result

def fs(args, node):
    _args = args
    _es_eng = _es_conn_ini(args=_args)
    _node = str(node)
    _query = q_fs
    _scroll = str(_args['scroll'])
    _size = int(_args['size'])
    _index = _args['pattern']
    _fs_dict = {}
    _result = []
    _today = '{0:%Y-%m-%d}'.format(datetime.datetime.today())

    try:
        _query['query']['bool']['must'][2]['match']['host.name'] = _node
    except Exception as _err:
        print('ERR: [getdata:diskio]', _err)
        return False
    else:
        try:
            _scan_res = elasticsearch.helpers.scan(client=_es_eng,
                                                   request_timeout=30,
                                                   query=_query,
                                                   scroll=_scroll,
                                                   size=_size,
                                                   index=_index,
                                                   clear_scroll=True,
                                                   raise_on_error=False)
        except Exception as _err:
            print('ERR: [getdata:diskio]', _err)
            return False
        else:
            _scan_res = list(_scan_res)
            if len(_scan_res) > 0:
                for _hit in _scan_res:
                    _filesystem_total = _hit['_source']['system']['filesystem']['total']
                    _filesystem_free = _hit['_source']['system']['filesystem']['free']
                    _filesystem_used_bytes = _hit['_source']['system']['filesystem']['used']['bytes']
                    _filesystem_used_pct = round((_hit['_source']['system']['filesystem']['used']['pct'] * 100), 2)

                    _filesystem_mount_point = _hit['_source']['system']['filesystem']['mount_point']
                    _filesystem_device_name = _hit['_source']['system']['filesystem']['device_name']

                    if _filesystem_mount_point not in _fs_dict.keys():
                        _fs_dict[_filesystem_mount_point] = {'filesystem_total': [],
                                                             'filesystem_free': [],
                                                             'filesystem_used_bytes': [],
                                                             'filesystem_used_pct': [],
                                                             'filesystem_device_name': _filesystem_device_name}

                    _fs_dict[_filesystem_mount_point]['filesystem_total'].append(_filesystem_total)
                    _fs_dict[_filesystem_mount_point]['filesystem_free'].append(_filesystem_free)
                    _fs_dict[_filesystem_mount_point]['filesystem_used_bytes'].append(_filesystem_used_bytes)
                    _fs_dict[_filesystem_mount_point]['filesystem_used_pct'].append(_filesystem_used_pct)

                for _filesystem_mount_point in _fs_dict.keys():
                    _result.append(json.dumps({'filesystem_total': round((statistics.mean(_fs_dict[_filesystem_mount_point]['filesystem_total'])), 2),
                                               'filesystem_free': round((statistics.mean(_fs_dict[_filesystem_mount_point]['filesystem_free'])), 2),
                                               'filesystem_used_bytes': round((statistics.mean(_fs_dict[_filesystem_mount_point]['filesystem_used_bytes'])), 2),
                                               'filesystem_used_pct': round((statistics.mean(_fs_dict[_filesystem_mount_point]['filesystem_used_pct'])), 2),
                                               'filesystem_device_name': _fs_dict[_filesystem_mount_point]['filesystem_device_name'],
                                               'filesystem_mount_point': _filesystem_mount_point,
                                               "node": _node,
                                               "@timestamp": _today,
                                               "metricset_module": "system",
                                               "metricset_name": "filesystem"}))

    return _result

def diskio(args, node):
    _args = args
    _es_eng = _es_conn_ini(args=_args)
    _node = str(node)
    _query = q_diskio
    _scroll = str(_args['scroll'])
    _size = int(_args['size'])
    _index = _args['pattern']
    _diskio_dict = {}
    _result = []
    _today = '{0:%Y-%m-%d}'.format(datetime.datetime.today())

    try:
        _query['query']['bool']['must'][2]['match']['host.name'] = _node
    except Exception as _err:
        print('ERR: [getdata:diskio]', _err)
        return False
    else:
        try:
            _scan_res = elasticsearch.helpers.scan(client=_es_eng,
                                                   request_timeout=30,
                                                   query=_query,
                                                   scroll=_scroll,
                                                   size=_size,
                                                   index=_index,
                                                   clear_scroll=True,
                                                   raise_on_error=False)
        except Exception as _err:
            print('ERR: [getdata:diskio]', _err)
            return False
        else:
            _scan_res = list(_scan_res)
            if len(_scan_res) > 0:
                for _hit in _scan_res:
                    if 'iostat' in _hit['_source']['system']['diskio'].keys():
                        try:
                            _diskio_iostat_read_await = _hit['_source']['system']['diskio']['iostat']['read']['await']
                            _diskio_iostat_read_per_sec_bytes = _hit['_source']['system']['diskio']['iostat']['read']['per_sec']['bytes']
                            _diskio_iostat_write_await = _hit['_source']['system']['diskio']['iostat']['write']['await']
                            _diskio_iostat_write_per_sec_bytes = _hit['_source']['system']['diskio']['iostat']['write']['per_sec']['bytes']

                            _diskio_name = _hit['_source']['system']['diskio']['name']
                        except Exception as _err:
                            print('ERR: [getdata:diskio]', _err)
                        else:
                            if _diskio_name not in _diskio_dict.keys():
                                _diskio_dict[_diskio_name] = {'diskio_iostat_read_await': [],
                                                             'diskio_iostat_read_per_sec_bytes': [],
                                                             'diskio_iostat_write_await': [],
                                                             'diskio_iostat_write_per_sec_bytes': [],
                                                             'diskio_name': []}

                            _diskio_dict[_diskio_name]['diskio_iostat_read_await'].append(_diskio_iostat_read_await)
                            _diskio_dict[_diskio_name]['diskio_iostat_read_per_sec_bytes'].append(_diskio_iostat_read_per_sec_bytes)
                            _diskio_dict[_diskio_name]['diskio_iostat_write_await'].append(_diskio_iostat_write_await)
                            _diskio_dict[_diskio_name]['diskio_iostat_write_per_sec_bytes'].append(_diskio_iostat_write_per_sec_bytes)

                for _diskio_name in _diskio_dict.keys():
                    _result.append(json.dumps({'diskio_iostat_read_await': round((statistics.mean(_diskio_dict[_diskio_name]['diskio_iostat_read_await'])), 2),
                                               'diskio_iostat_read_per_sec_bytes': round((statistics.mean(_diskio_dict[_diskio_name]['diskio_iostat_read_per_sec_bytes'])), 2),
                                               'diskio_iostat_write_await': round((statistics.mean(_diskio_dict[_diskio_name]['diskio_iostat_write_await'])), 2),
                                               'diskio_iostat_write_per_sec_bytes': round((statistics.mean(_diskio_dict[_diskio_name]['diskio_iostat_write_per_sec_bytes'])), 2),
                                               'diskio_name': _diskio_name,
                                               "node": _node,
                                               "@timestamp": _today,
                                               "metricset_module": "system",
                                               "metricset_name": "diskio"}))
    return _result

def load(args, node):
    _args = args
    _es_eng = _es_conn_ini(args=_args)
    _node = str(node)
    _query = q_load
    _scroll = str(_args['scroll'])
    _size = int(_args['size'])
    _index = _args['pattern']
    _load_dict = {'load_1': [],
                 'load_5': [],
                 'load_15': []}
    _result = []
    _today = '{0:%Y-%m-%d}'.format(datetime.datetime.today())

    try:
        _query['query']['bool']['must'][2]['match']['host.name'] = _node
    except Exception as _err:
        print('ERR: [getdata:load]', _err)
        return False
    else:
        try:
            _scan_res = elasticsearch.helpers.scan(client=_es_eng,
                                                   request_timeout=30,
                                                   query=_query,
                                                   scroll=_scroll,
                                                   size=_size,
                                                   index=_index,
                                                   clear_scroll=True,
                                                   raise_on_error=False)
        except Exception as _err:
            print('ERR: [getdata:load]', _err)
            return False
        else:
            _scan_res = list(_scan_res)
            if len(_scan_res) > 0:
                for _hit in _scan_res:
                    try:
                        _load_1 = _hit['_source']['system']['load']['1']
                        _load_5 = _hit['_source']['system']['load']['5']
                        _load_15 = _hit['_source']['system']['load']['15']
                    except Exception as _err:
                        print('ERR: [getdata:load]', _err)
                    else:
                        _load_dict['load_1'].append(_load_1)
                        _load_dict['load_5'].append(_load_5)
                        _load_dict['load_15'].append(_load_15)

                _result.append(json.dumps({'load_1': round((statistics.mean(_load_dict['load_1'])), 2),
                                           'load_5': round((statistics.mean(_load_dict['load_5'])), 2),
                                           'load_15': round((statistics.mean(_load_dict['load_15'])), 2),
                                           "node": _node,
                                           "@timestamp": _today,
                                           "metricset_module": "system",
                                           "metricset_name": "load"}))

    return _result