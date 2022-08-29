from sqlitedict import SqliteDict
import asyncio


class AsyncListCache:
    def __init__(self, file: str, cache_name: str = "list") -> None:
        self._file = file
        self.db = SqliteDict(self._file, autocommit=True)
        self._list_key = cache_name
        self.list = self._get()

    async def update(self):
        def _update():
            self.db[self._list_key] = self.list.copy()
        t = asyncio.get_event_loop().run_in_executor(None, lambda: _update())
        while not t.done():
            await asyncio.sleep(0.1)

    def _get(self):
        try:
            return self.db[self._list_key]
        except KeyError:
            return []

    async def append(self, item: str):
        self.list.append(item)
        await self.update()

    async def remove(self, item: str):
        self.remove(item)
        await self.update()

    def __contains__(self, item):
        return item in self.list

    def __str__(self) -> str:
        return str(self.list)

    def __repr__(self) -> str:
        return str(self.list)
