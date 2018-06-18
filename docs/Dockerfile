# htpasswd pw:  Un1vers1tet

FROM        nginx:latest
MAINTAINER  Francesco de Virgilio <francesco.devirgilio@ubiquitypress.com>

RUN         apt-get -y update && apt-get -y install supervisor

COPY        supervisord.conf /etc/supervisor/supervisord.conf
COPY        nginx.conf /etc/nginx/nginx.conf
COPY        ./build/html /usr/share/nginx/html/docs

RUN         chown -R www-data:www-data /usr/share/nginx/html/docs

# Expose HTTP port
EXPOSE      80

# Last but least, unleach the daemon!
ENTRYPOINT  ["/usr/bin/supervisord"]
