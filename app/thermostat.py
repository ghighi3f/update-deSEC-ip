import tinytuya
import requests
from time import sleep
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
THERMOSTAT_IP = os.environ.get('THERMOSTAT_IP')

def send_message(message):
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
  requests.get(url).json()

# Connect to Device
d = tinytuya.OutletDevice(
    dev_id='bfa598511b15f3606aray8',
    address=THERMOSTAT_IP,      # Or set to 'Auto' to auto-discover IP address
    local_key='IwL;ntFas:t}:O#+',
    version=3.4,
    persist=True)

data = d.status()

logging.info(" > Send Request for Status < ")
d.status(nowait=True)

logging.info(" > Begin Monitor Loop <")
while (True):
  # See if any data is available
  data = d.receive()
  if (data):
    if ('dps' in data and '3' in data['dps'] and data['dps']['3'] == 'idle'):
      logging.info('Heater is turned off.')
      send_message('Heater is turned off.')
    elif ('dps' in data and '3' in data['dps'] and data['dps']['3'] == 'heating'):
      logging.info('Heater is turned on.')
      send_message('Heater is turned on.')

  # Send keep-alive heartbeat
  if not data:
    d.heartbeat()

  # NOTE If you are not seeing updates, you can force them - uncomment:
  # print(" > Send Request for Status < ")
  # d.status(nowait=True)

  # NOTE Some smart plugs require an UPDATEDPS command to update power data
  # print(" > Send DPS Update Request < ")
  # payload = d.generate_payload(tinytuya.UPDATEDPS)
  # d.send(payload)
