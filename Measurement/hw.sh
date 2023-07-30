#!/bin/bash

# disk finder 
lsblk -no NAME | grep -o '^sd[a-z]' > ./disks.txt
