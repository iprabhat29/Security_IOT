#!/bin/bash
echo "CREATING USER $1"
mosquitto_passwd -b passwordfile $1 $2
echo "DONE!!"
