#!/usr/bin/env bash

CONTAINER_NAME="crawl4ai"
IMAGE_NAME="docker.io/unclecode/crawl4ai:latest" # 0.6.0-r1

case "$1" in
  start)
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
      echo "Container already running"
    else
      if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
        echo "Starting existing container"
        docker start $CONTAINER_NAME
      else
        echo "Creating new container"
        docker run -d -p 11235:11235 --name $CONTAINER_NAME --shm-size=1g $IMAGE_NAME
      fi
    fi
    echo "crawl4ai available at http://127.0.0.1:11235/playground"
    ;;
  stop)
    docker stop $CONTAINER_NAME
    ;;
  status)
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
      echo "crawl4ai is running"
      echo "UI available at http://127.0.0.1:11235/playground"
    else
      echo "crawl4ai is not running"
    fi
    ;;
  logs)
    docker logs $CONTAINER_NAME
    ;;
  restart)
    docker stop $CONTAINER_NAME
    docker start $CONTAINER_NAME
    ;;
  rm)
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME
    ;;
  *)
    echo "Usage: crawl4ai-docker {start|stop|status|logs|restart|rm}"
    ;;
esac
