#!/bin/bash

echo "Starting Web Application"
docker compose up -d
echo "Web Application is available at http://127.0.0.1"
echo "VS Code Server is available at http://127.0.0.1:8443"
