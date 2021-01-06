import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import sys
import re
from time import time, localtime, strftime, sleep
import telebot
import requests
from Levenshtein import distance as levenshtein_distance
import config
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

    
    

dictmap = {}

def load_dict(code,fn):
  dictmap[code] = [] 
  with open(fn,"r") as f:
    for l in f:
      if l.startswith('#') or l.startswith(' '):
        continue
      m = re.search(r'^(\S+)\s(\S+)', l)
      if not m:
        print ("ERROR: [%s]" % l)
        continue
      m1 = m.group(1)
      m2 = m.group(2)
      dictmap[code].append((m1, m2))

def translate(code, text):
  for k,v in dictmap[code]:
    text = re.sub(k, v, text)
  return text

load_dict("glag2cyrl","glag2cyrl.tab")
load_dict("tfng2cyrl","tfng2cyrl.tab")
load_dict("cyrl2glag","cyrl2glag.tab")
load_dict("cyrl2tfng","cyrl2tfng.tab")

# команда /rules для @mikitkinabeseda
@bot.message_handler(commands=["rules"])
def rules(message):
  if message.chat.type in ['group','supergroup'] and message.chat.id == -1001199017575:
    with open("rules.md", "r") as f:
      rules = f.read()
    bot.send_message(message.chat.id, rules, parse_mode="Markdown")

@bot.message_handler(content_types=['text'])
def translate_message(message):
  msg = message.text
  print ("%s|%s <%s %s> %s" % (str(message.chat.id), strftime("%Y-%m-%d %H:%M:%S", localtime(message.date)), message.from_user.first_name, message.from_user.last_name, msg))
  if time() > message.date+config.max_timediff:
    print (" message time too old :(")
    return
  for code in config.default_tabs:
    msgtr = translate(code, msg)
    dist = levenshtein_distance(msg, msgtr)
    ratio = dist/len(msg)
    if ratio > config.min_levenshtein_ratio:
      print (" code=%s ratio=%lf => %s" % (code, ratio, msgtr))
      try:
        if config.test_mode:
          msgtr = "[TEST MODE] "+msgtr
        bot.send_message(message.chat.id, msgtr, reply_to_message_id=message.message_id)
      except telebot.apihelper.ApiException:
        print (" Exception occured!")
      return

# inline-режим, у боевого бота выключен, так как нельзя запретить использовать его в конкретном чате
@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(inline_query):
  print (inline_query)
  msgtr_glag = translate('cyrl2glag', inline_query.query)
  msgtr_tfng = translate('cyrl2tfng', inline_query.query)
  if config.test_mode:
    msgtr_glag = "[TEST MODE] "+msgtr_glag
    msgtr_tfng = "[TEST MODE] "+msgtr_tfng
  r_glag = telebot.types.InlineQueryResultArticle('GLAG', f'{inline_query.query} -> {msgtr_glag}', telebot.types.InputTextMessageContent(msgtr_glag))
  r_tfng = telebot.types.InlineQueryResultArticle('TFNG', f'{inline_query.query} -> {msgtr_tfng}', telebot.types.InputTextMessageContent(msgtr_tfng))
  bot.answer_inline_query(inline_query.id, [r_glag, r_tfng])
    
    
    

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
