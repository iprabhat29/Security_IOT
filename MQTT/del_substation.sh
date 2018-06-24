echo "Deleting USER $1"
mosquitto_passwd -D passwordfile $1
