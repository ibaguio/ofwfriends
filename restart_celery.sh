#!/bin/bash
echo -n "[+] Stopping Celery daemon..."
celery multi stop worker -A pinder -B
echo -e "[\e[92mOK\e[0m]"

sleep 1

echo -n "[+] Starting Celery daemon..."
celery multi start worker -A pinder -B
echo -e "[\e[92mOK\e[0m]"

