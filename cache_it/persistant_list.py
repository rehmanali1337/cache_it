import os
import pickle
import asyncio


class PersistantList:

    def __init__(self, key):
        self._dir = "cache"
        if not os.path.exists(self._dir):
            os.makedirs(self._dir)
        self._list_file = f'{self._dir}/{key}'
        self._list = list()
        if os.path.exists(self._list_file):
            with open(self._list_file, "rb") as f:
                self._list = pickle.load(f)
        else:
            self._list = list()
        self._lock = asyncio.Lock()

    def _persist(self):
        with open(self._list_file, "wb") as f:
            pickle.dump(self._list, f)

    def __repr__(self):
        return str(self._list)

    async def append(self, value):
        async with self._lock:
            self._list.append(value)
            self._persist()

    async def remove(self, value):
        async with self._lock:
            self._list.remove(value)
            self._persist()

    def __contains__(self, value):
        return value in self._list
