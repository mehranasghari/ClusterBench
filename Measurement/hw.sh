#!/bin/bash
lsblk -no NAME | grep -o '^sd[a-z]' > ./disks.txt
