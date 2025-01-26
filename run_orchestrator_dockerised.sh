#!/bin/bash

# Exit on error
set -e

# Variables
CONTAINER_NAME="orchestrator-container"
IMAGE_NAME="orchestrator"
PORT_MAPPING="8000:8000"

# Check if the script is run with sudo or as root
if [ "$EUID" -ne 0 ]; then
  echo "Error: This script must be run with sudo or as the root user."
  exit 1
fi

# Build the Docker image
echo "Building Docker image '$IMAGE_NAME'"
docker build -t $IMAGE_NAME .

# Check if a container with the same name already exists
if [ "$(docker ps -aq -f name=^${CONTAINER_NAME}$)" ]; then
  echo "Container '$CONTAINER_NAME' already exists."

  # Check if the container is running
  if [ "$(docker ps -q -f name=^${CONTAINER_NAME}$)" ]; then
    echo "Stopping the running container..."
    docker stop $CONTAINER_NAME
  fi

  # Remove the existing container
  echo "Removing the existing container"
  docker rm $CONTAINER_NAME
fi

# Run the container in detached mode
echo "Starting a new container '$CONTAINER_NAME'"
docker run -d --name $CONTAINER_NAME -p $PORT_MAPPING $IMAGE_NAME

echo "Container '$CONTAINER_NAME' is now running and accessible on port $PORT_MAPPING."
