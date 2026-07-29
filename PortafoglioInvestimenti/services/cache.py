"""
services/cache.py

Cache generica per dati temporanei.
Utilizzata inizialmente per le quotazioni.
"""

from __future__ import annotations

from datetime import datetime, timedelta


class CacheItem:

    def __init__(self, value, ttl=300):

        self.value = value
        self.expire = datetime.now() + timedelta(seconds=ttl)

    @property
    def expired(self):

        return datetime.now() >= self.expire


class Cache:

    def __init__(self):

        self._items = {}

    def put(self, key, value, ttl=300):

        self._items[key] = CacheItem(value, ttl)

    def get(self, key):

        item = self._items.get(key)

        if item is None:
            return None

        if item.expired:
            del self._items[key]
            return None

        return item.value

    def remove(self, key):

        self._items.pop(key, None)

    def clear(self):

        self._items.clear()

    def contains(self, key):

        return self.get(key) is not None

    def size(self):

        return len(self._items)

    def cleanup(self):

        expired = []

        for key, item in self._items.items():

            if item.expired:
                expired.append(key)

        for key in expired:
            del self._items[key]