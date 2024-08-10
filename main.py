import os
import time
from datetime import datetime
import logging

from dotenv import load_dotenv

import httpx

from web3 import Web3

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler

from pymongo import MongoClient
from mongopersistence import MongoPersistence

from query import Deployment

load_dotenv()

MONGODB_CONNECTION_URI = os.getenv("MONGODB_CONNECTION_URI")
TELEGRAM_KEY = os.getenv("TELEGRAM_KEY")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# MongoDB setup
mongodb_client = MongoClient(MONGODB_CONNECTION_URI)
db = mongodb_client['telegram_db']
wallet_data = db['wallet_data']

persistence = MongoPersistence(
    mongo_url=MONGODB_CONNECTION_URI,
    db_name="telegram_db",
    name_col_user_data="user_data",  # optional
    name_col_bot_data="bot_data",
    name_col_chat_data="chat_data",
    create_col_if_not_exist=True,  # optional
    ignore_general_data=["cache"],
    ignore_user_data=["foo", "bar"],
    load_on_flush=False,
    update_interval=60
)

WALLET = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Start")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text('Welcome! Please enter your wallet address.', reply_markup=reply_markup)
    print(update.message.chat.id)

    return WALLET

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    wallet_address = update.message.text
    is_wallet = Web3.is_address(wallet_address)

    if not is_wallet:
        await update.message.reply_text("Invalid wallet address. Please enter a valid wallet address.")
        return WALLET
    wallet_address = str(Web3.to_checksum_address(wallet_address))
    logger.info("User %s entered wallet address: %s", user.first_name, wallet_address)
    await update.message.reply_text(f"Thank you! Your wallet {wallet_address} has been registered. You will now receive notifications for liquidations and redemptions against your vessels.")
    wallet_data.insert_one({"user_id": user.id, "wallet_address": wallet_address})

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_KEY).persistence(persistence).build()
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WALLET: [MessageHandler(filters.CHAT, wallet)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        persistent=True,
        name="entry_conv"
    )

    application.add_handler(conv_handler)

    application.run_polling()



















