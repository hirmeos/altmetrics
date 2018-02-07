FROM python:3.6.4-alpine3.7

#RUN apt-get -y update
#RUN apt-get install -y libpq-dev
#RUN apt-get install -y git

RUN apk update && apk -U upgrade && \
    apk add python-dev postgresql-dev git openssh-client gcc musl-dev \
    gcc-avr g++ bash && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    mkdir /hirmeos_metrics && \
    pip install --upgrade pip && \
    pip install git+https://github.com/Supervisor/supervisor.git && \
    pip install gunicorn

ADD supervisord.conf /etc/
ADD requirements.txt .
RUN pip install -r requirements.txt && \
    rm requirements.txt
ADD live_config.ini /hirmeos_metrics
ADD config.ini /hermios_metrics
ADD . /hirmeos_metrics/
ENV DJANGO_SETTINGS_MODULE core.settings_live
RUN cd /hirmeos_metrics/src && mkdir /static && ./manage.py collectstatic