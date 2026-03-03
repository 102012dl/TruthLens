"""
TruthLens Telegram bot — aiogram 3.x async.

Commands:
- /start — welcome
- /analyze <text> — analyze arbitrary text
- /trends <query> — keyword trends for topic
- /news <query> — analyzed news articles for topic
- /help — show help

The bot calls the FastAPI backend (env BACKEND_URL, default http://localhost:8000)
using httpx and formats responses with Markdown. During processing it displays
“⏳ Аналізую...” to the user.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any

import httpx
from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
router = Router()


def _build_backend_url(path: str) -> str:
    """Join BACKEND_URL with an API path."""

    return f"{BACKEND_URL.rstrip('/')}{path}"


def _extract_arg(text: str, command: str) -> str:
    """Extract argument after command name from the full message text."""

    if not text:
        return ""
    # e.g. "/analyze some text" or "/analyze@bot some text"
    parts = text.split(maxsplit=1)
    if not parts:
        return ""
    if len(parts) == 1:
        return ""
    return parts[1].strip()


def _format_analysis(payload: dict[str, Any]) -> str:
    """Format /api/analyze response as Markdown."""

    sentiment = payload.get("sentiment") or {}
    entities = payload.get("entities") or []
    fake_news = payload.get("fake_news") or payload.get("fake_news_score")
    text_length = payload.get("text_length")

    label = sentiment.get("label", "N/A")
    score = sentiment.get("score", 0.0)
    stars = sentiment.get("stars", 0)

    lines: list[str] = []
    lines.append(f"*Результати аналізу:*")
    lines.append(f"- *Сентимент*: `{label}` (⭐ {stars}, score={score:.2f})")
    if fake_news is not None:
        lines.append(f"- *Ймовірність фейку*: `{fake_news:.2f}`")
    if text_length is not None:
        lines.append(f"- *Довжина тексту*: `{text_length}` символів")

    if entities:
        lines.append("")
        lines.append("*Виявлені сутності:*")
        for ent in entities[:10]:
            ent_text = ent.get("text", "")
            label_ = ent.get("label", "")
            lang = ent.get("language") or ""
            extra = f" ({lang})" if lang else ""
            lines.append(f"- `{ent_text}` — {label_}{extra}")

    return "\n".join(lines)


def _format_news_list(articles: list[dict[str, Any]]) -> str:
    """Format analyzed articles list as Markdown."""

    if not articles:
        return "Не знайдено новин за цим запитом."

    lines: list[str] = ["*Топ новини:*"]
    for idx, art in enumerate(articles[:10], start=1):
        title = art.get("title") or "Без назви"
        url = art.get("url")
        source = art.get("source") or "N/A"
        sent = art.get("sentiment") or {}
        stars = sent.get("stars", "?")
        fake_news = art.get("fake_news")
        fake_str = f"{fake_news:.2f}" if isinstance(fake_news, (int, float)) else "N/A"
        if url:
            title_md = f"[{title}]({url})"
        else:
            title_md = title
        lines.append(f"{idx}. {title_md} — `{source}` (⭐ {stars}, фейк={fake_str})")
    return "\n".join(lines)


def _format_trends(trends: list[dict[str, Any]]) -> str:
    """Format trends keywords as Markdown."""

    if not trends:
        return "Трендових ключових слів не знайдено."

    lines: list[str] = ["*Трендові ключові слова:*"]
    for t in trends[:20]:
        kw = t.get("keyword") or t.get("term") or t.get("word")
        if not kw:
            continue
        score = t.get("score")
        if isinstance(score, (int, float)):
            lines.append(f"- `{kw}` (score={score:.2f})")
        else:
            lines.append(f"- `{kw}`")
    return "\n".join(lines)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Handle /start — welcome and short help."""

    text = (
        "👋 *Ласкаво просимо до TruthLens Bot!*\n\n"
        "Це бот для інтелектуального аналізу новин та текстів.\n\n"
        "*Команди:*\n"
        "- `/analyze <текст>` — аналіз тексту (сентимент, сутності, фейковість)\n"
        "- `/trends <тема>` — трендові ключові слова за темою\n"
        "- `/news <тема>` — останні новини з аналізом\n"
        "- `/help` — показати цю довідку\n"
    )
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Handle /help — show command list."""

    await cmd_start(message)


@router.message(Command("analyze"))
async def cmd_analyze(message: Message) -> None:
    """Handle /analyze <text> — call POST /api/analyze and reply with result."""

    arg = _extract_arg(message.text or "", "/analyze")
    if not arg:
        await message.answer(
            "Будь ласка, надішліть команду у форматі:\n`/analyze ваш текст для аналізу`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    loading = await message.answer("⏳ Аналізую...", parse_mode=ParseMode.MARKDOWN)

    url = _build_backend_url("/api/analyze")
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(url, json={"text": arg})
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        await loading.edit_text(
            f"Не вдалося виконати аналіз.\n`{exc}`", parse_mode=ParseMode.MARKDOWN
        )
        return

    formatted = _format_analysis(data)
    await loading.edit_text(formatted, parse_mode=ParseMode.MARKDOWN)


@router.message(Command("news"))
async def cmd_news(message: Message) -> None:
    """Handle /news <query> — call POST /api/news/search."""

    arg = _extract_arg(message.text or "", "/news")
    if not arg:
        await message.answer(
            "Будь ласка, надішліть команду у форматі:\n`/news тема або запит`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    loading = await message.answer("⏳ Аналізую...", parse_mode=ParseMode.MARKDOWN)
    url = _build_backend_url("/api/news/search")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                url, json={"query": arg, "language": "en", "days": 1}
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        await loading.edit_text(
            f"Не вдалося отримати новини.\n`{exc}`", parse_mode=ParseMode.MARKDOWN
        )
        return

    articles = data.get("articles") or []
    formatted = _format_news_list(articles)
    await loading.edit_text(formatted, parse_mode=ParseMode.MARKDOWN)


@router.message(Command("trends"))
async def cmd_trends(message: Message) -> None:
    """Handle /trends <query> — call POST /api/trends."""

    arg = _extract_arg(message.text or "", "/trends")
    if not arg:
        await message.answer(
            "Будь ласка, надішліть команду у форматі:\n`/trends тема або запит`",
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    loading = await message.answer("⏳ Аналізую...", parse_mode=ParseMode.MARKDOWN)
    url = _build_backend_url("/api/trends")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                url, json={"query": arg, "language": "en", "days": 7}
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        await loading.edit_text(
            f"Не вдалося отримати тренди.\n`{exc}`", parse_mode=ParseMode.MARKDOWN
        )
        return

    trends = data.get("keywords") or []
    formatted = _format_trends(trends)
    await loading.edit_text(formatted, parse_mode=ParseMode.MARKDOWN)


def main() -> None:
    """Run bot. Requires env TELEGRAM_BOT_TOKEN and optionally BACKEND_URL."""

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is required")

    async def _run() -> None:
        bot = Bot(token=token, parse_mode=ParseMode.MARKDOWN)
        dp = Dispatcher()
        dp.include_router(router)
        await dp.start_polling(bot)

    asyncio.run(_run())


if __name__ == "__main__":
    main()

