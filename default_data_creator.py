#!/usr/bin/python
# -*- coding: utf-8 -*-

from farado.items.user import User
from farado.items.meta_item_manager import MetaItemManager

if __name__ == '__main__':
    manager = MetaItemManager()
    user = User(
        'admin',
        'John',
        'Ivanovich',
        'Smith',
        'john.smith@ivanovich.com',
        password="admin",
        )
    manager.add_item(user)
