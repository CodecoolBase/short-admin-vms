#!/bin/sh -eux
apt-get -y install apache2
a2enmod userdir
# wget \
#   --recursive \
#   --page-requisites \
#   --adjust-extension \
#   --span-hosts \
#   --convert-links \
#   --domains www.theworldsworstwebsiteever.com,theworldsworstwebsiteever.com \
#   --no-parent \
#   https://www.theworldsworstwebsiteever.com/
wget $FILE_SERVER_URL/www.theworldsworstwebsiteever.com.zip
unzip -od /var/www/html www.theworldsworstwebsiteever.com.zip
systemctl enable apache2
systemctl restart apache2
