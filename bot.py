import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1205938982:AAHtuIxO4Y55fOFCy3GQnpuC8IAUi9R7n7s'

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Bajına"""
    update.message.reply_text('Hi!')

def help(update, context):
    """Amcıx"""
    update.message.reply_text('Help!')

    
    


runic_dict = {
    "ing": "\u16DD",
    "ae": "\u16AB",
    "th": "\u16A6",
    "ea": "\u16E0",
    "ia": "\u16e1",
    "io": "\u16e1",
    "oe": "\u16DF",
    "ee": "\u16DF",
    "gh": "\u16B8",
    "kh": "\u16E4",
    "a": "\u16AA",
    "b": "\u16D2",
    "c": "\u16B3",
    "d": "\u16DE",
    "e": "\u16D6",
    "f": "\u16A0",
    "g": "\u16B7",
    "h": "\u16BB",
    "i": "\u16C1",
    "j": "\u16C4",
    "k": "\u16e3",
    "l": "\u16DA",
    "m": "\u16D7",
    "n": "\u16BE",
    "o": "\u16A9",
    "p": "\u16C8",
    "q": "\u16E2",
    "r": "\u16B1",
    "s": "\u16CB",
    "t": "\u16CF",
    "u": "\u16A2",
    #        "v":"\u16A2",
    "v": "\u16A1",  # medieval version
    "w": "\u16B9",
    "x": "\u16C9",
    "y": "\u16A3",
    "z": "\u16CE",
    " ": "\u16eb",
    ",\u16eb": " \u16ec ",
    ";\u16eb": " \u16ec ",
    ":\u16eb": " \u16ec ",
    ".\u16eb": " \u16ed ",
    "?\u16eb": " \u16ed ",
    "!\u16eb": " \u16ed ",
    "'\u16eb": " \u16eb ",
    "'": " \u16eb ",
    ",": " \u16ec ",
    ";": " \u16ec ",
    ":": " \u16ec ",
    ".": " \u16ed ",
    "?": " \u16ed ",
    "!": " \u16ed ",
    '"': "",
}


def runify(text):
    text = text.lower()
    for k, v in runic_dict.items():
        text = text.replace(k, v)
    return text
    
    
    

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """İ am not your friend. my friend"""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://bitig-bot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
