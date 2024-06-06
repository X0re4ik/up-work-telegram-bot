import asyncio
import logging
import sys

from src.bot import BOT
from src.handles import dp


async def main() -> None:
    await dp.start_polling(BOT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())