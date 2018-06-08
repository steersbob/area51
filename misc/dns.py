import asyncio
import aiodns


async def do():
    for i in range(10):
        print('doing...')
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
resolver = aiodns.DNSResolver(loop=loop)
f = resolver.query('eventbus', 'A')
f2 = do()
result = loop.run_until_complete(
    asyncio.wait([f, f2], return_when=asyncio.FIRST_COMPLETED)
)
print(result)
