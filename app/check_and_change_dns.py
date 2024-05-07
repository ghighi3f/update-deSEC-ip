import requests
import json
from time import sleep
import logging
import random
import re
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
DESEC_DOMAIN = os.environ.get('DESEC_DOMAIN')
DESEC_TOKEN = os.environ.get('DESEC_TOKEN')


def is_ipv4_address(ip):
  return bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip))


def get_current_wan_ip():
  urls = [
      'https://checkip.amazonaws.com/',
      'https://ifconfig.io/ip',
      'https://icanhazip.com/'
  ]

  # Randomising which endpoint is used to not abuse.
  random.shuffle(urls)
  for url in urls:
    try:
      response = requests.get(url)
      response.raise_for_status()
      logging.info(f"Got IP from {url}!")
      ip = response.text.strip()
      if is_ipv4_address(ip):
        return ip  # Return if successful
      else:
        logging.warning(f"IP format is wrong - {ip}")
    except requests.exceptions.RequestException as e:
      logging.warning(f"Error with {url}: {e}")

    logging.error(
        "Cannot get WAN IP; possibly a connection issue, retrying in 5 minutes...")


def getDeSecIp():
  url = f"https://desec.io/api/v1/domains/{DESEC_DOMAIN}/rrsets/"
  headers = {'Authorization': f"Token {DESEC_TOKEN}"}
  try:
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    logging.info(f"Got DeSeC IP from {url}!")
    domain = next(
        (item for item in response.json() if item['type'] == 'A'),
        None
    )
    if domain:
      return domain['records'][0]  # Return if successful
    else:
      logging.warning(f"Cannot get DeSeC IP; possibly a connection issue")
  except requests.exceptions.RequestException as e:
    logging.warning(f"Error with {url}: {e}")


def send_message(wan_ip):
  reply_markup = {"inline_keyboard": [
      [{"text": "Yes", "callback_data": wan_ip}, {"text": "No", "callback_data": "no"}]]}
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
  requests.post(url=url, data={"chat_id": CHAT_ID, 'text': f"IP has changed to: {wan_ip}. Change IP ?",
                'reply_markup': json.dumps(reply_markup)}).json()


if __name__ == '__main__':
  # Loop to check for IP changes
  while True:
    new_wan_ip = get_current_wan_ip()
    deSec_ip = getDeSecIp()
    logging.info(f"Current WAN IP: {new_wan_ip}")
    logging.info(f"Current DeSec IP: {deSec_ip}")
    if new_wan_ip != deSec_ip:
      logging.info(f"WAN IP changed to: {new_wan_ip}.  Asking for update...")
      send_message(new_wan_ip)

    else:
      logging.info("No change in WAN IP. No update needed.")

    # Wait for 15 minutes before checking again
    sleep(int(900))
