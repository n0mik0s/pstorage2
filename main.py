import argparse
import os
import pprint

from cfgenerator import cfgenerator
from mappings import *
from getdata import *
from putdata import *

if __name__=="__main__":
    pp = pprint.PrettyPrinter(indent=4)

    argparser = argparse.ArgumentParser(usage='%(prog)s [options]')
    argparser.add_argument('-c', '--conf',
                           help='Set full path to the configuration file.',
                           default='conf.default.yml')
    argparser.add_argument('-v', '--verbose',
                           help='Set verbose run to true.',
                           action='store_true')

    getdata_args = argparser.parse_args()

    verbose = getdata_args.verbose
    root_dir = os.path.dirname(os.path.realpath(__file__))
    conf_path_full = str(root_dir) + os.sep + str(getdata_args.conf)

    cf = cfgenerator(cf_path=conf_path_full)

    if verbose: pp.pprint(cf)

    if not (('es_getdata' in cf) and ('es_putdata' in cf)):
        print('ERR: [main]: Check config file: es_getdata or es_putdata block are absent.')
        exit(1)

    try:
        es_getdata_nodes = cf['es_getdata']['nodes']

        es_getdata_conn_ca_cert = str(root_dir) + os.sep + str(cf['es_getdata']['conn']['ca_cert'])
        es_getdata_conn_port = cf['es_getdata']['conn']['port']
        es_getdata_conn_use_ssl = cf['es_getdata']['conn']['use_ssl']
        es_getdata_conn_verify_certs = cf['es_getdata']['conn']['verify_certs']
        es_getdata_index_pattern = cf['es_getdata']['index']['pattern']
        es_getdata_index_user = cf['es_getdata']['index']['user']
        es_getdata_index_password = cf['es_getdata']['index']['password']
        es_getdata_helpers_scan_request_timeout = cf['es_getdata']['helpers_scan']['request_timeout']
        es_getdata_helpers_scan_scroll = cf['es_getdata']['helpers_scan']['scroll']
        es_getdata_helpers_scan_size = cf['es_getdata']['helpers_scan']['size']

        es_putdata_nodes = cf['es_putdata']['nodes']
        es_putdata_conn_ca_cert = str(root_dir) + os.sep + str(cf['es_putdata']['conn']['ca_cert'])
        es_putdata_conn_port = cf['es_putdata']['conn']['port']
        es_putdata_conn_use_ssl = cf['es_putdata']['conn']['use_ssl']
        es_putdata_conn_verify_certs = cf['es_putdata']['conn']['verify_certs']
        es_putdata_index_pattern = cf['es_putdata']['index']['pattern']
        es_putdata_index_user = cf['es_putdata']['index']['user']
        es_putdata_index_password = cf['es_putdata']['index']['password']
        es_putdata_index_shards = cf['es_putdata']['index']['shards']
        es_putdata_index_replicas = cf['es_putdata']['index']['replicas']
    except Exception as err:
        print('ERR: [main]: There is an error with property', err, 'in the provided conf file.')
        exit(1)
    else:
        try:
            metrics = cf['metrics']
        except Exception as err:
            print('ERR: [main]: There is an error with property', err, 'in the provided conf file.')
            exit(1)
        else:
            try:
                nodes_list = cf['nodes_list']
            except Exception as err:
                print('ERR: [main]: There is an error with property', err, 'in the provided conf file.')
                exit(1)
            else:
                for metric in metrics:
                    if verbose: print('INF: [main]: Next metric will be processed:', metric)
                    for nodename in nodes_list:
                        if verbose: print('INF: [main]: Next node will be processed:', nodename)

                        getdata_args = {'es_nodes': es_getdata_nodes,
                                        'ca_cert': es_getdata_conn_ca_cert,
                                        'port': es_getdata_conn_port,
                                        'use_ssl': es_getdata_conn_use_ssl,
                                        'verify_certs': es_getdata_conn_verify_certs,
                                        'pattern': es_getdata_index_pattern,
                                        'user': es_getdata_index_user,
                                        'password': es_getdata_index_password,
                                        'request_timeout': es_getdata_helpers_scan_request_timeout,
                                        'scroll': es_getdata_helpers_scan_scroll,
                                        'size': es_getdata_helpers_scan_size}

                        putdata_args = {'es_nodes': es_putdata_nodes,
                                        'ca_cert': es_putdata_conn_ca_cert,
                                        'port': es_putdata_conn_port,
                                        'use_ssl': es_putdata_conn_use_ssl,
                                        'verify_certs': es_putdata_conn_verify_certs,
                                        'pattern': es_putdata_index_pattern,
                                        'user': es_putdata_index_user,
                                        'password': es_putdata_index_password,
                                        'shards': es_putdata_index_shards,
                                        'replicas': es_putdata_index_replicas,
                                        'mapping': out_index_map}

                        if 'cpu' in metric:
                            result = cpu(args=getdata_args, node=nodename)
                            elastic_bulk_insert(args=putdata_args, js_arr=result)
                            if verbose: print(result)
                        elif 'memory' in metric:
                            result = memory(args=getdata_args, node=nodename)
                            elastic_bulk_insert(args=putdata_args, js_arr=result)
                            if verbose: print(result)
                        elif 'fs' in metric:
                            result = fs(args=getdata_args, node=nodename)
                            elastic_bulk_insert(args=putdata_args, js_arr=result)
                            if verbose: print(result)
                        elif 'diskio' in metric:
                            result = diskio(args=getdata_args, node=nodename)
                            elastic_bulk_insert(args=putdata_args, js_arr=result)
                            if verbose: print(result)
                        elif 'load' in metric:
                            result = load(args=getdata_args, node=nodename)
                            elastic_bulk_insert(args=putdata_args, js_arr=result)
                            if verbose: print(result)
                        else:
                            print('ERR: [main]: There is an error with metric', metric)