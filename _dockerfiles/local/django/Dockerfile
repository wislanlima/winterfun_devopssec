FROM python:3.10.0-slim-buster

ENV APP_HOME=/app
ADD . /app/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

LABEL decription="Development image for Winter Fun"

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  && apt-get install -y gettext \
  && apt-get install -y make \
  && apt-get install -y nano \
  && apt-get -y install netcat gcc postgresql \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

COPY ./winterfun/templates/css/avatar.png /app/mediafiles/avatar.png

RUN pip3 install -r requirements.txt

COPY ./_dockerfiles/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./_dockerfiles/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start







ENTRYPOINT [ "/entrypoint"]
