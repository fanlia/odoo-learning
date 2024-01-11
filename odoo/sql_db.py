

import psycopg2
import odoo

def connection_info_for(db_name):
    connection_info = {'database': db_name, 'application_name': 'odoo'}
    for p in ('host', 'port', 'user', 'password'):
        cfg = odoo.tools.config['db_' + p]
        if cfg:
            connection_info[p] = cfg

    return connection_info

def db_connect(db_name):
    info = connection_info_for(db_name)
    print(info)
    conn = psycopg2.connect(**info)
    return conn
