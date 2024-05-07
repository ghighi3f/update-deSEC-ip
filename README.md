
# Update deSEC IP
Python script in docker container that checks once every 15 min if the WAN IP address changes, in which case it will send a notification to an existing telegram bot chat with the option to update a deSEC domain with the new IP address.


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file in the root folder

`TELEGRAM_TOKEN`

`TELEGRAM_CHAT_ID`

`DESEC_TOKEN`

`DESEC_DOMAIN`



## Run

Made to work with docker compose

```bash
  docker-compose up -d
```
    
## Documentation

How to get Telegram Bot Token - [Documentation](https://core.telegram.org/bots/tutorial#introduction)
How to get Telegram Chat ID - [Stack Overflow answer](https://stackoverflow.com/a/32572159/10412138)
