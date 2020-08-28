#this project dont depend to buttonbot.py and main.py dont work, its still unnecessary, but there are some codes that may be usefule

import datetime
from subprocess import Popen
from subprocess import PIPE

from telegram import Bot
from telegram import Update
from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler

from apis.bittrex import BittrexClient
from apis.bittrex import BittrexError
from echo.config import load_config

CALLBACK_BUTTON1_LEFT = "callback_button1_left"
CALLBACK_BUTTON2_RIGHT = "callback_button2_right"
CALLBACK_BUTTON3_MORE = "callback_button3_more"
CALLBACK_BUTTON4_BACK = "callback_button4_back"
CALLBACK_BUTTON5_TIME = "callback_button5_time"
CALLBACK_BUTTON6_PRICE = "callback_button6_price"
CALLBACK_BUTTON7_PRICE = "callback_button7_price"
CALLBACK_BUTTON8_PRICE = "callback_button8_price"

TITLES = {
    CALLBACK_BUTTON1_LEFT: "new message",
    CALLBACK_BUTTON2_RIGHT: "Change settings",
    CALLBACK_BUTTON3_MORE: "More",
    CALLBACK_BUTTON4_BACK: "back",
    CALLBACK_BUTTON5_TIME: "time",
    CALLBACK_BUTTON6_PRICE: "BTC",
    CALLBACK_BUTTON7_PRICE: "LTC",
    CALLBACK_BUTTON8_PRICE: "ETH",
}


config = load_config()
client = BittrexClient()

def get_base_inline_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_TIME], callback_data=CALLBACK_BUTTON5_TIME),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_PRICE], callback_data=CALLBACK_BUTTON6_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_PRICE], callback_data=CALLBACK_BUTTON7_PRICE),
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON8_PRICE], callback_data=CALLBACK_BUTTON8_PRICE),
        ],
        [
            InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def keyboard_callback_handler(bot: Bot, update: Update, chat_data=None, **kwargs):

    query = update.callback_query
    data = query.data
    now = datetime.datetime.now()
    
    if data == CALLBACK_BUTTON1_LEFT:
        query.edit_message_text(
            text = current_text,
            parse_mode=ParseMode.MARKDOWN,
        )

        bot.send_message(
            chat_id = chat_id,
            text = "New message\n\ncallback_query.data={}".format(data),
            reply_markup=get_base_inline_keyboard(),
        )

    elif data == CALLBACK_BUTTON2_RIGHT:
        query.edit_message_text(
            text="Succesfully changed in {}".format(now),
            reply_markup=get_base_inline_keyboard(),

        )
    elif data == CALLBACK_BUTTON3_MORE:

        query.edit_message_text(
            text=current_text,
            reply_markup=get_keyboard2(),
        )
    elif data == CALLBACK_BUTTON4_BACK:
        query.edit_message_text(
            text=current_text,
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON5_TIME:
        text = "*Time now*\n\n{}".format(now)
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup = get_keyboard2(),
        )
    elif data in (CALLBACK_BUTTON6_PRICE, CALLBACK_BUTTON7_PRICE, CALLBACK_BUTTON8_PRICE):
        pair = {
            CALLBACK_BUTTON6_PRICE: "USD-BTC",
            CALLBACK_BUTTON7_PRICE: "USD-LTC",
            CALLBACK_BUTTON8_PRICE: "USD-ETH",
        }[data]

        try:
            current_price = client.get_last_price(pair=pair)
            text = "Valute corse:\n\n{} = {}$".format(pair, current_price)
        except BittrexError:
            text = "Error"
        query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_keyboard2(),
        )

def do_start(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="hello! Send me something",
        reply_markup=get_base_inline_keyboard(),
    )

def do_help(bot: Bot, update: Update):
    bot.send_message(
        chat_id=update.message.chat_id,
    )

        