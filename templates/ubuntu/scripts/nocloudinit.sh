#!/bin/sh -eux
if [ -d /etc/cloud/cloud.cfg.d ]
then
  sh -c "echo 'datasource_list: [ None ]' > /etc/cloud/cloud.cfg.d/90_dpkg.cfg"
  apt-get purge -y cloud-init
  rm -rf /etc/cloud
  rm -rf /var/lib/cloud
fi
