#!/bin/bash


sed -i "/\[sql\]/aconnection = postgresql://keystone:password@$DB_PORT_5432_TCP_ADDR:$DB_PORT_5432_TCP_PORT/keystone?client_encoding=utf8" /etc/keystone.conf.sample

# Wait for postgres to start
STATUS=2

while [ $STATUS -ne 0 ]
do
    PGPASSWORD=password psql -h $DB_PORT_5432_TCP_ADDR -p $DB_PORT_5432_TCP_PORT -U keystone -c 'select 1'
    STATUS=$?
    sleep 1
done

keystone-manage --config-file /etc/keystone.conf.sample db_sync

keystone-all --config-file /etc/keystone.conf.sample
