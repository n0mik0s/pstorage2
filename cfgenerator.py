import yaml

def cfgenerator(cf_path):
    _cf_path = cf_path
    _cf = False

    with open(_cf_path, 'r') as _reader:
        try:
            _cf = yaml.safe_load(_reader)
        except yaml.YAMLError as _err:
            print('ERR: [cfgenerator:cfgenerator]', _err)
            return _cf
        else:
            return _cf