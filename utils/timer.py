import asyncio

async def handle_timer(callback, interval_seconds):
    while True:
        callback()
        print(f"Timer invoked. Waiting another {interval_seconds} seconds...")
        await asyncio.sleep(interval_seconds)