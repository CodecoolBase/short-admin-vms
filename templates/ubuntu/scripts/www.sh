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
mount /dev/sr1 /media
unzip -od /var/www/html /media/www.theworldsworstwebsiteever.com.zip
umount /dev/sr1
systemctl enable apache2
systemctl restart apache2
