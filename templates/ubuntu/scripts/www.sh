#!/bin/sh -eux
apt-get -y install apache2 p7zip-full
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
last_cdrom_device=$(ls -1 /dev/sr* | sort | tail -1)
dd if=$last_cdrom_device of=files.iso
7z x files.iso -o.
rm files.iso
unzip -od /var/www/html www.theworldsworstwebsiteever.com.zip
systemctl enable apache2
systemctl restart apache2
# 7z is needed to extract the ISO mounted by Packer
# if it contains long filenames (Joliet ISO extension)
apt-get remove p7zip-full
