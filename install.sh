#!/bin/bash

HOME_DIR=/opt/cesclient
CACHE_DIR=/mnt/storage/cesclient-cache

useradd -G cesbox -p '*' -u 1101 -s /bin/bash --user-group --create-home cesclient

DIRS="$CACHE_DIR/logs $CACHE_DIR/downloads/ready $HOME_DIR"
mkdir -p $DIRS

#ARIA2C_BIN=$HOME_DIR/aria2c
#wget -O $ARIA2C_BIN  http://terra-media.ru:8080/cesclient/aria2c
#chmod +x $ARIA2C_BIN

TMP=/tmp/current.tar.gz
wget -O $TMP  http://terra-media.ru/cesclient/cesclient-current.tar.gz
tar -xzvf $TMP -C $HOME_DIR

chown -R cesclient.cesclient $CACHE_DIR

chown -R cesbox.cesbox /mnt/storage/cesbox/portal/
chmod g+w /mnt/storage/cesbox/portal/

cp $HOME_DIR/conf/cesclient_lr.conf /etc/logrotate.d
# uuid and token
# wget -O cesclient_install.sh http://terra-media.ru/cesclient/install.sh
# chmod +x cesclient_install.sh
# cesclient_install.sh
