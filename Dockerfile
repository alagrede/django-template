FROM ubuntu:14.04

MAINTAINER Anthony LAGREDE <lagrede.lagrede@gmail.fr>

# Install env
RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential && \
  apt-get install -y software-properties-common && \
  apt-get install -y byobu curl git htop man unzip vim wget && \
  rm -rf /var/lib/apt/lists/*


# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /var/www/mysite

RUN apt-get update && apt-get install -qq -y apache2 nano python-software-properties build-essential fontconfig


RUN apt-get install -y mysql-server python-pip build-essential python-dev libmysqlclient-dev
# Pour mysql & ldap
RUN apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
RUN apt-get install python-mysqldb
RUN apt-get install libmysqlclient-dev
RUN apt-get install libapache2-mod-wsgi


# ouverture du port 81
EXPOSE 80


WORKDIR /etc/apache2/sites-enabled

ADD docker/apache/ports.conf /etc/apache2/
RUN ln -s /var/www/django-template/mysite/mysite.conf mysite.conf


# conf du back
RUN a2enmod proxy_http
RUN a2dissite 000-default.conf

# script de demarrage
ADD docker/start.sh /usr/local/bin/start.sh

WORKDIR /var/www/django-template/

CMD ["/usr/local/bin/start.sh"]
