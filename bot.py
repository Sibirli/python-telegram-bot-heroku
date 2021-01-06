import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import sys
import re
from collections import OrderedDict
from functools import reduce
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

    
    

cli_mode = len(sys.argv) > 1

if not cli_mode:
    import telebot
    bot = telebot.TeleBot('1205938982:AAHtuIxO4Y55fOFCy3GQnpuC8IAUi9R7n7s')

bitig_soft_digraph_dict = OrderedDict([
    ('rö',    '𐰼𐰇'),
    ('yal',    '𐰖𐰞'),
    ('tj',    'ть'),
    ('dj',    'дь'),
    ('lj',    'ль'),
    ('nj',    'нь'),
    ('rj',    'рь'),
    ('sj',    'сь'),
    ('zj',    'зь'),
    ('tsj',   'ць'),
    ('tcj',   'чь'),
])

bitig_apostrophe_digraph_dict = OrderedDict([
    ('rö',    '𐰼𐰇'),
    ('yal',    '𐰖𐰞'),
    ('qj',    'ґʼj'),
    ('kj',    'кʼj'),
    ('fj',    'фʼj'),
    ('vj',    'вʼj'),
    ('wj',    'ввʼj'),
    ('hj',    'гʼj'),
    ('xj',    'хʼj'),
    ('mj',    'мʼj'),
    ('svja',  'свя'), # *ь non-normal // tbh no need, but current OG-fags
    ('tsvja', 'цвя'),
    ('dzvja', 'дзвя'),
    ('tjmja', 'тьмя'),
])

bitig_jotted_digraph_dict = OrderedDict([
    ('ja',    'я'),
    ('je',    'є'),
    ('ji',    'ї'),
    ('jy',    'ї'),
    ('ju',    'ю'),
])

bitig_letter_dict = OrderedDict([
    ('ctc',   'щ'),
    ('tc',    'ч'),
    ('ts',    'ц'),
    ('a',     'а'),
    ('b',     'б'),
    ('c',     'ш'),
    ('d',     'д'),
    ('e',     'е'),
    ('f',     'ф'),
    ('g',     'ж'),
    ('h',     'г'),
    ('i',     'і'),
    ('j',     'й'),
    ('k',     'к'),
    ('l',     'л'),
    ('m',     'м'),
    ('n',     'н'),
    ('o',     'о'),
    ('ö',     '𐰇'),
    ('p',     'п'),
    ('q',     'ґ'),
    ('r',     'р'),
    ('s',     'с'),
    ('t',     'т'),
    ('u',     'у'),
    ('v',     'в'),
    ('w',     'вв'),
    ('x',     'х'),
    ('y',     '𐰖'),
    ('z',     'з'),
    ('\'',    'ʼ'),
])

patterns_dicts = [(re.compile("(%s)" % '|'.join(dict.keys())), dict) for dict in (
    bitig_soft_digraph_dict,
    bitig_apostrophe_digraph_dict,
    bitig_jotted_digraph_dict,
    bitig_letter_dict,
)]



def is_bitik(str):
    return re.search(r"[a-z\']", str)



def xlate(s, pattern_dict):
    regex, dict = pattern_dict
    return regex.sub(lambda x: dict[x.group()], s)


def xlate_all(s):
    return reduce(xlate, patterns_dicts, s)


if cli_mode:
    bitik = str(sys.argv[1]).lower()
    if is_bitik(bitik):
        runes = xlate_all(bitik)
        print(runes)
else:
    @bot.message_handler(content_types=['text', 'photo'])
    @bot.edited_message_handler(content_types=['text', 'photo'])
    def reply(message):
        if message.content_type == 'text':
            bitik = message.text
        else:
            bitik = message.caption
        bitik = bitik.lower()
        if is_bitik(bitik):
            runes = xlate_all(bitik)
            bot.send_message(message.chat.id, runes)
    
    
    

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
