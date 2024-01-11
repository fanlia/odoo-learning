
import logging
import threading
import werkzeug
import os
import odoo
from odoo.tools import config

_logger = logging.getLogger(__name__)

def load_server_wide_modules():
    server_wide_modules = odoo.tools.config['server_wide_modules'].split(',')

    for m in server_wide_modules:
        odoo.modules.load_openerp_module(m)

def preload_registries(dbnames):
    rc = 0
    for dbname in dbnames:
        update_module = config.get('init') or config.get('update')
        registry = odoo.modules.registry.Registry.new(dbname, update_module=update_module)

    return rc

class ThreadedServer(object):
    def __init__(self, app):
        self.app = app
        self.interface = config.get('http_interface', '0.0.0.0')
        self.port = config.get('http_port', 8069)

    def start(self, stop=False):
        if not stop:
            werkzeug.serving.run_simple(self.interface, self.port, self.app, use_debugger=True, use_reloader=True)

    def stop(self):
        odoo.sql_db.close_all()

    def run(self, preload=None, stop=False):
        rc = preload_registries(preload)
        self.start(stop=stop)
        if stop:
            self.stop()
        return rc

server = None

def start(preload=None, stop=False):
    global server
    print('service.server.start')

    load_server_wide_modules()
    server = ThreadedServer(odoo.http.root)
    rc = server.run(preload, stop)
    return rc
