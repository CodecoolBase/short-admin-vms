#!/bin/sh -eux
apt-get -y install postgresql
sudo -u postgres -- $SHELL <<EOF
createuser -s "$BASE_USER"
createdb -O "$BASE_USER" "$BASE_USER"
psql -c "ALTER USER $BASE_USER WITH PASSWORD '$BASE_PASS';"
EOF
config_file=$(sudo -iu postgres psql -t -P format=unaligned -c 'SHOW config_file')
hba_file=$(sudo -iu postgres psql -t -P format=unaligned -c 'SHOW hba_file')
sed -E -i "s,^#listen_addresses\s+=\s+'[^']+'(.*)$,listen_addresses = '*'\1\t," $config_file
echo 'host    all             all             0.0.0.0/0               md5' >> $hba_file
systemctl restart postgresql
