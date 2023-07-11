#!/bin/bash

echo "Welcome to cos-bench"
echo "1 -> Backup"
echo "2 -> Restore"
echo -n "Enter the number of the action to perform: "
read number

case $number in
    1)
        echo "Running backup"
        ./app/send_load.sh
        ;;
    2)
        echo "Running restore"
        python3 ./query-convertor/2.py -d /mnt/sdb/influx-test/influxdb-data/tarred-files
        ;;
    *)
        echo "Unknown Process"
        ;;
esac
