#!/bin/sh -eux
apt-get -y install postgresql
sudo -u postgres -- $SHELL <<EOF
createuser -s "$ADMIN_USER"
createdb -O "$ADMIN_USER" "$ADMIN_USER"
psql -c "ALTER USER $ADMIN_USER WITH PASSWORD '$ADMIN_PASS';"
EOF
config_file=$(sudo -iu postgres psql -t -P format=unaligned -c 'SHOW config_file')
hba_file=$(sudo -iu postgres psql -t -P format=unaligned -c 'SHOW hba_file')
sed -E -i "s,^#listen_addresses\s+=\s+'[^']+'(.*)$,listen_addresses = '*'\1\t," $config_file
echo 'host    all             all             0.0.0.0/0               md5' >> $hba_file
systemctl restart postgresql
