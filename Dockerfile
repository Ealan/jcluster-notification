FROM python:3

RUN apt-get update && apt-get install -y \
    cron \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools \
 && pip install \
    requests \
    beautifulsoup4 \
    cchardet

RUN echo '* * * * * root /usr/local/bin/python /data/notification.py' >> /etc/crontab

WORKDIR /data

CMD ["cron", "-f"]

