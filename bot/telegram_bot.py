"""
TruthLens Telegram bot — aiogram 3.x async.

Commands: /start, /analyze, /trends, /news.
Calls backend API (env BACKEND_URL) for analysis and news.
"""

from __future__ import annotations

import os
from typing import Any

# TODO: aiogram 3.x
# from aiogram import Bot, Dispatcher, F
# from aiogram.filters import Command
# from aiogram.types import Message
# import aiohttp


async def cmd_start(message: "Message") -> None:
    """Handle /start — welcome and short help."""
    await message.answer(
        "TruthLens — News Intelligence Bot. Commands: /analyze, /trends, /news"
    )


async def cmd_analyze(message: "Message") -> None:
    """Handle /analyze <text> — call POST /api/analyze and reply with result."""
    # TODO: parse text, call backend, format reply
    await message.answer("Not implemented: call backend /api/analyze")


async def cmd_trends(message: "Message") -> None:
    """Handle /trends <query> — call POST /api/trends."""
    # TODO: call backend /api/trends
    await message.answer("Not implemented: call backend /api/trends")


async def cmd_news(message: "Message") -> None:
    """Handle /news <query> — call POST /api/news/search."""
    # TODO: call backend /api/news/search
    await message.answer("Not implemented: call backend /api/news/search")


def main() -> None:
    """Run bot. Requires env TELEGRAM_BOT_TOKEN and optionally BACKEND_URL."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is required")
    # TODO: Bot(token=token), Dispatcher(), register handlers, dp.start_polling()
    raise NotImplementedError("Wire aiogram Bot/Dispatcher and start polling")


if __name__ == "__main__":
    main()
