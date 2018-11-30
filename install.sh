#!/bin/bash

SERVICE_NAME=ardtime.service
SERVICE_PATH=/lib/systemd/system/$SERVICE_NAME

echo "[*] Installing Ardtime service"
sudo cp $SERVICE_NAME $SERVICE_PATH
sudo chmod 644 $SERVICE_PATH

echo "[*] Reloading systemd"
sudo systemctl daemon-reload

echo "[*] Enable $SERVICE_NAME at boot"
sudo systemctl enable $SERVICE_NAME

echo "[*] Checking artime status"
sudo systemctl status $SERVICE_NAME
