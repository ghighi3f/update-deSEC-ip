FROM python:alpine

WORKDIR /usr/src/app

RUN apk add --no-cache bash

RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
RUN chmod +x check_and_change_dns.py
RUN chmod +x bot.py
RUN chmod +x thermostat.py
RUN chmod +x docker_entrypoint.sh

ENTRYPOINT ["/usr/src/app/docker_entrypoint.sh"]