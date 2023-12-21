import asyncio


async def async_example(name, delay):
    print(f"Hello, {name}! Start sleeping for {delay} seconds.")
    await asyncio.sleep(delay)
    print(f"Hello, {name}! Finished sleeping for {delay} seconds.")


async def main():
    tasks = [
        async_example("Alice", 2),
        async_example("Bob", 1),
        async_example("Charlie", 3),
    ]

    # Run tasks concurrently
    await asyncio.gather(*tasks)

# Run the main coroutine
if __name__ == "__main__":
    asyncio.run(main())
