FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    gettext \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

RUN echo "#!/bin/sh\n\
    python manage.py makemigrations\n\
    python manage.py migrate\n\
    python manage.py collectstatic --noinput\n\
    gunicorn --workers=4 config.wsgi:application --bind 0.0.0.0:8000" > /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
