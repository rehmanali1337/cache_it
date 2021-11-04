import os
import pickle
import asyncio


class PersistantDict:

    def __init__(self, name):
        self._dir = "cache"
        if not os.path.exists(self._dir):
            os.makedirs(self._dir)
        self._dict_file = f'{self._dir}/{name}'
        self._dict = dict()
        if os.path.exists(self._dict_file):
            with open(self._dict_file, "rb") as f:
                self._dict = pickle.load(f)
        else:
            self._dict = dict()
        self._lock = asyncio.Lock()

    def _persist(self):
        with open(self._dict_file, "wb") as f:
            pickle.dump(self._dict, f)

    def __repr__(self):
        return str(self._dict)

    async def add(self, key, value):
        async with self._lock:
            self._dict[key] = value
            self._persist()

    async def remove(self, key):
        async with self._lock:
            self._dict.pop(key, None)
            self._persist()

    async def get(self, key):
        return self._dict.get(key, None)

    def __contains__(self, value):
        return value in self._dict.keys()

    def values(self):
        return self._dict.values()

    def keys(self):
        return self._dict.keys()
