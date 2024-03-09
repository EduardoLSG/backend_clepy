FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
EXPOSE 5432
WORKDIR /app
COPY . /app

RUN apt-get update && apt-get -y install cron vim

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir
RUN python manage.py collectstatic
RUN python manage.py crontab add