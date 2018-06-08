import asyncio
import aio_pika


async def talk():
    while True:
        print('something')
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.wait(
            [
                aio_pika.connect_robust("amqp://guest:guest@127.0.0.1", loop=loop),
                talk()
            ]
        )
    )
    loop.close()
