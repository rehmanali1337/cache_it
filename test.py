from cache_it import PersistantDict
import asyncio


async def test():
    d = PersistantDict("di")
    print(await d.get("Hello"))

asyncio.run(test())
