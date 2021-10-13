FROM python:3.9-slim

WORKDIR /usr/src/app
RUN apt-get update && apt-get -y install cron vim && apt-get clean

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN chmod +x /usr/src/app/run-cron.sh

# CMD cron && tail -f /var/log/cron.log
ENTRYPOINT [ "/usr/src/app/run-cron.sh" ]

