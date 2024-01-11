
import time
import logging
from collections.abc import Mapping

import odoo

_logger = logging.getLogger(__name__)
_schema = logging.getLogger('odoo.schema')

class Registry(Mapping):
    def registries(cls):
        return {}

    def __new__(cls, db_name):
        try:
            return cls.registries[db_name]
        except KeyError:
            return cls.new(db_name)

    @classmethod
    def new(cls, db_name, update_module=False):
        t0 = time.time()
        registry = object.__new__(cls)
        registry.init(db_name)

        odoo.modules.load_modules(registry, update_module)
        _logger.info("Registry loaded in %.3fs", time.time() - t0)
        return registry

    @classmethod
    def delete(cls, db_name):
        if db_name in cls.registries:
            del cls.registries[db_name]

    def init(self, db_name):
        self.models = {}
        self.db_name = db_name
        self._db = odoo.sql_db.db_connect(db_name)

    def __len__(self):
        return len(self.models)

    def __iter__(self):
        return iter(self.models)

    def __getitem__(self, model_name):
        return self.models[model_name]
