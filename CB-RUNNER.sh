#!/bin/bash

echo "Welcome to cos-bench"
echo "1 -> Backup"
echo "2 -> Restore"
echo -n "Enter the number of the action to perform: "
read number

case $number in
    1)
        bash $PWD/app/send_load.sh
        #./send_load.sh
        echo "Running backup"
        ;;
    2)
        echo "Running restore"
        python3 ./query-convertor/2.py -d /mnt/sdb/influx-test/influxdb-data/tarred-files
        ;;
    *)
        echo "Unknown Process"
        ;;
esac
