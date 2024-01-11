

import psycopg2
import odoo

def connection_info_for(db_name):
    connection_info = {'database': db_name, 'application_name': 'odoo'}
    for p in ('host', 'port', 'user', 'password'):
        cfg = odoo.tools.config['db_' + p]
        if cfg:
            connection_info[p] = cfg

    return connection_info

_Pool = {}

def db_connect(db_name):
    global _Pool
    if _Pool.get(db_name) is None:
        info = connection_info_for(db_name)
        print(info)
        _Pool[db_name] = psycopg2.connect(**info)
    return _Pool[db_name]

def close_db(db_name):
    global _Pool
    if _Pool.get(db_name):
        _Pool[db_name].close()
        del _Pool[db_name]
