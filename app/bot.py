#!/usr/bin/env python
# pylint: disable=unused-argument

import logging
import requests
from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, ContextTypes
import re
import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
DESEC_DOMAIN = os.environ.get('DESEC_DOMAIN')
DESEC_TOKEN = os.environ.get('DESEC_TOKEN')


def is_ipv4_address(ip):
  return bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip))


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """Parses the CallbackQuery and updates the message text."""
  query = update.callback_query

  # CallbackQueries need to be answered, even if no notification to the user is needed
  # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
  await query.answer()

  if is_ipv4_address(query.data):
    await query.edit_message_text(text=f"Updating IP: ~ {query.data} ~ ...")
    setDeSecIp(query.data)
  else:
    query.edit_message_text(text=f"Ok, aborting")


def setDeSecIp(ip):
  url = f"https://update.dedyn.io/?hostname={DESEC_DOMAIN}&myipv4={ip}"
  headers = {'Authorization': f"Token {DESEC_TOKEN}"}
  try:
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    logging.info(f"Updated DeSeC IP!")
    send_message(f"Updated DeSec IP! New IP: {ip}")
  except requests.exceptions.RequestException as e:
    logging.warning(f"Error with {url}: {e}")
    send_message(f"There was an error! :( Please check the logs.")


def send_message(message):
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
  requests.post(url=url, data={"chat_id": CHAT_ID, 'text': message}).json()


def main() -> None:
  """Run the bot."""
  # Create the Application and pass it your bot's token.
  application = Application.builder().token(TOKEN).build()
  application.add_handler(CallbackQueryHandler(button))

  # Run the bot until the user presses Ctrl-C
  application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
  main()
