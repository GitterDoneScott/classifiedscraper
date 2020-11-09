FROM python:3.7.0

WORKDIR /usr/src/app
RUN apt-get update && apt-get -y install cron vim

RUN pip install --upgrade pip
#pip freeze > requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

#every hour
RUN echo "0 * * * * root cd /usr/src/app && /usr/local/bin/scrapy crawl pinkbike >> /var/log/cron.log 2>&1" >> /etc/cron.d/platform-location
RUN echo "0 * * * * root cd /usr/src/app && /usr/local/bin/scrapy crawl craigslist >> /var/log/cron.log 2>&1" >> /etc/cron.d/platform-location
RUN chmod 0644 /etc/cron.d/platform-location
RUN touch /var/log/cron.log
CMD cron && tail -f /var/log/cron.log
