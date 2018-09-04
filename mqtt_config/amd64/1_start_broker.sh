# Run a Mosquitto Docker container on Raspberry Pi

# https://store.docker.com/community/images/pascaldevink/rpi-mosquitto

# place your mosquitto.conf in /srv/mqtt/config/
# NOTE: You have to change the permissions of the directories
# to allow the user to read/write to data and log and read from
# config directory
# For TESTING purposes you can use chmod -R 777 /srv/mqtt/*
# Better use "-u" with a valid user id on your docker host

# on Raspberry Pi
# copy mqtt/config mqtt/log mqtt/data on to RPi under /data/elastic_network_of_things_with_mqtt_and_micropython/mqtt
# grand permission for user

sudo chmod -R 777 /data/elastic_network_of_things_with_mqtt_and_micropython/mqtt_config/amd64/mqtt/*

docker run -d -p 1883:1883 -p 9001:9001 --name=Mosquitto --hostname=Mosquitto \
--volume=/data/elastic_network_of_things_with_mqtt_and_micropython/mqtt_config/amd64/mqtt/config:/mosquitto/config:ro \
--volume=/data/elastic_network_of_things_with_mqtt_and_micropython/mqtt_config/amd64/mqtt/data:/mosquitto/data \
--volume=/data/elastic_network_of_things_with_mqtt_and_micropython/mqtt_config/amd64/mqtt/log:/mosquitto/log \
eclipse-mosquitto

