FROM python:3.6.4-alpine3.7

RUN apk update && apk -U upgrade && \
    apk add postgresql-dev git openssh-client gcc musl-dev \
    gcc-avr g++ bash && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    mkdir /hirmeos_metrics && \
    pip install --upgrade pip && \
    pip install git+https://github.com/Supervisor/supervisor.git@5cd53ce66d79b51e0f6979f18bf3608fd6864f95 && \
    pip install gunicorn

ADD requirements.txt .
RUN pip install -r requirements.txt && \
    rm requirements.txt
ADD . /hirmeos_metrics/
RUN cd /hirmeos_metrics/src && mkdir /static && ./manage.py collectstatic
ADD supervisord.conf /etc/
CMD /usr/local/bin/supervisord