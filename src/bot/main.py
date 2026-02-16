"""
TruthLens - Telegram Bot
========================
Aiogram 3.x based Telegram bot for credibility analysis

Author: 102012dl
Email: 102012dl@gmail.com
"""

import asyncio
import os
import logging
from typing import Optional

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.ml.analyzer import create_analyzer, TruthLensAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== Bot Configuration =====

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Initialize bot and dispatcher
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Global analyzer
analyzer: Optional[TruthLensAnalyzer] = None

# ===== Keyboards =====

def get_main_keyboard() -> InlineKeyboardMarkup:
    """Create main menu keyboard."""
    keyboard = [
        [InlineKeyboardButton(text="🔍 Аналізувати текст", callback_data="analyze")],
        [InlineKeyboardButton(text="📊 Моя статистика", callback_data="stats")],
        [InlineKeyboardButton(text="ℹ️ Про TruthLens", callback_data="about")],
        [InlineKeyboardButton(text="⚙️ Налаштування", callback_data="settings")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_score_emoji(score: int) -> str:
    """Get emoji based on credibility score."""
    if score >= 80:
        return "🟢"  # Green
    elif score >= 60:
        return "🟡"  # Yellow
    elif score >= 40:
        return "🟠"  # Orange
    else:
        return "🔴"  # Red

# ===== Handlers =====

@dp.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command."""
    welcome_text = """
🔍 <b>TruthLens</b> - Ваш помічник у боротьбі з дезінформацією!

Я допоможу вам:
• Перевірити достовірність новини
• Виявити маніпуляції та упередження
• Оцінити надійність джерела
• Проаналізувати емоційне забарвлення

📝 <b>Як користуватись:</b>
Просто надішліть мені текст новини або посилання!

Оберіть дію:
    """
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    help_text = """
📚 <b>Довідка TruthLens</b>

<b>Команди:</b>
/start - Почати роботу
/help - Довідка
/analyze - Аналіз тексту
/stats - Статистика
/about - Про бота

<b>Оцінка достовірності:</b>
🟢 80-100% - Достовірно
🟡 60-79% - Скоріше правда
🟠 40-59% - Невизначено
🔴 0-39% - Сумнівно
    """
    await message.answer(help_text)

@dp.message(Command("about"))
async def cmd_about(message: Message):
    """Handle /about command."""
    about_text = """
🔍 <b>TruthLens v1.0.0</b>

AI-платформа для аналізу достовірності інформації.

<b>Технології:</b>
• ML/NLP аналіз (BERT, spaCy)
• Sentiment Analysis
• Bias Detection
• Fact-Checking (RAG)

<b>Розробник:</b>
102012dl@gmail.com

<b>Capstone Project | Neoversity</b>
    """
    await message.answer(about_text)

@dp.message(F.text)
async def handle_text(message: Message):
    """Handle text messages - perform analysis."""
    global analyzer
    
    if analyzer is None:
        analyzer = create_analyzer()
        await analyzer.load_models()
    
    text = message.text
    
    # Check minimum length
    if len(text) < 20:
        await message.answer(
            "⚠️ Текст занадто короткий для аналізу.\n"
            "Надішліть більше тексту (мінімум 20 символів)."
        )
        return
    
    # Send "analyzing" message
    status_msg = await message.answer("🔄 Аналізую текст...")
    
    try:
        # Perform analysis
        result = await analyzer.analyze(text)
        
        # Format response
        emoji = get_score_emoji(result.credibility_score)
        
        response = f"""
{emoji} <b>Результат аналізу</b>

🎯 <b>Оцінка достовірності:</b> {result.credibility_score}%
🏷 <b>Вердикт:</b> {result.verdict}

📊 <b>Детальний аналіз:</b>
• Тональність: {result.sentiment.value}
• Упередженість: {result.bias_level}
• Маніпуляції: {len(result.manipulative_techniques)} виявлено

🔍 <b>Ключові висновки:</b>
"""
        for finding in result.key_findings[:3]:
            response += f"• {finding}\n"
        
        response += "\n💡 <b>Рекомендації:</b>\n"
        for rec in result.recommendations[:2]:
            response += f"• {rec}\n"
        
        response += f"\n⏱ Час аналізу: {result.processing_time_ms}мс"
        
        # Delete status message and send result
        await status_msg.delete()
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        await status_msg.edit_text(
            "❌ Помилка при аналізі. Спробуйте пізніше."
        )

# ===== Callback Handlers =====

@dp.callback_query(F.data == "analyze")
async def callback_analyze(callback: types.CallbackQuery):
    await callback.message.answer(
        "📝 Надішліть мені текст новини для аналізу."
    )
    await callback.answer()

@dp.callback_query(F.data == "about")
async def callback_about(callback: types.CallbackQuery):
    await cmd_about(callback.message)
    await callback.answer()

@dp.callback_query(F.data == "stats")
async def callback_stats(callback: types.CallbackQuery):
    await callback.message.answer(
        "📊 <b>Ваша статистика:</b>\n\n"
        "• Запитів сьогодні: 0\n"
        "• Всього аналізів: 0\n"
        "• Середня оцінка: --"
    )
    await callback.answer()

@dp.callback_query(F.data == "settings")
async def callback_settings(callback: types.CallbackQuery):
    await callback.message.answer(
        "⚙️ <b>Налаштування:</b>\n\n"
        "• Мова: Українська\n"
        "• Детальний аналіз: Увімкнено\n"
        "• План: Free"
    )
    await callback.answer()

# ===== Main =====

async def main():
    """Main function to run the bot."""
    global analyzer
    
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return
    
    logger.info("Starting TruthLens bot...")
    
    # Initialize analyzer
    analyzer = create_analyzer()
    await analyzer.load_models()
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
