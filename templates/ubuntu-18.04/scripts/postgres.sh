#!/bin/sh -eux
apt-get -y install postgresql
sudo -u postgres -- $SHELL <<EOF
createuser -s ubuntu
createdb -O ubuntu ubuntu
psql -c "ALTER USER ubuntu WITH PASSWORD 'ubuntu';"
EOF
sed -E -i "s,^#listen_addresses\s+=\s+'[^']+'(.*)$,listen_addresses = '*'\1\t," /etc/postgresql/10/main/postgresql.conf
echo 'host    all             all             0.0.0.0/0               md5' >> /etc/postgresql/10/main/pg_hba.conf
systemctl restart postgresql
