#!/usr/bin/python
# -*- coding: utf-8 -*-

from farado.items.user import User
from farado.items.meta_item_manager import MetaItemManager
from farado.config import farado_config



if __name__ == '__main__':
    manager = MetaItemManager(farado_config['database']['connection_string'])
    user = User(
        'admin',
        'John',
        'Ivanovich',
        'Smith',
        'john.smith@ivanovich.com',
        password="admin",
        )
    manager.add_item(user)
