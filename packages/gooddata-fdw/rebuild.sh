#!/bin/bash
# (C) 2021 GoodData Corporation

if [ -z "$1" ]; then
  echo "Usage: $0 <service_name>"
  echo ""
  echo "Use this script for rebuilding services, including volume if exists."
  exit 1
fi

DC_FILES="-f docker-compose.yaml"
SERVICE=$1

echo "[SERVICE $SERVICE] Delete container ..."
docker-compose $DC_FILES rm -fsv "$SERVICE"

echo "[SERVICE $SERVICE] Build image, if relevant ..."
docker-compose $DC_FILES build

VOLUME="$(docker volume ls | grep "${PWD##*/}_$SERVICE"-data | awk '{print $2}')"
if [ -n "$VOLUME" ]; then
  echo "[SERVICE $SERVICE] Delete volume ..."
  docker volume rm "$VOLUME"
fi

echo "[SERVICE $SERVICE] Start from scratch ..."
docker-compose $DC_FILES up -d "$SERVICE"
