#!/bin/bash

ENV_VARS_FILE="/root/container.env"
CRON_FILE="/root/cron_schedule"

echo "Dumping env variables into ${ENV_VARS_FILE}"
declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > ${ENV_VARS_FILE}

# Setup a cron schedule
echo "SHELL=/bin/bash" >> ${CRON_FILE}
echo "BASH_ENV=${ENV_VARS_FILE}" >> ${CRON_FILE}
echo "* * * * * echo 'Cron is alive!' > /proc/1/fd/1 2>/proc/1/fd/2" >> ${CRON_FILE}
#list crawlers and run them sequentially with xargs
echo "0 */2 * * * cd /usr/src/app && /usr/local/bin/scrapy list| xargs -n 1 /usr/local/bin/scrapy crawl > /proc/1/fd/1 2>/proc/1/fd/2" >> ${CRON_FILE}
#echo "0 * * * * cd /usr/src/app && /usr/local/bin/scrapy crawl pinkbike > /proc/1/fd/1 2>/proc/1/fd/2" >> ${CRON_FILE}
#echo "0 * * * * cd /usr/src/app && /usr/local/bin/scrapy crawl craigslist > /proc/1/fd/1 2>/proc/1/fd/2" >> ${CRON_FILE}
#echo "0 * * * * cd /usr/src/app && /usr/local/bin/scrapy crawl facebook > /proc/1/fd/1 2>/proc/1/fd/2" >> ${CRON_FILE}
#echo "0 * * * * cd /usr/src/app && /usr/local/bin/scrapy crawl ebay > /proc/1/fd/1 2>/proc/1/fd/2" >> ${CRON_FILE}
echo "#empty line" >> ${CRON_FILE}

#installing cron schedule
crontab ${CRON_FILE}

echo "Running cron"
cron -f