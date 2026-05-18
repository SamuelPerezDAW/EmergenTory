#!/bin/bash

echo '----- Buildeando la API -----'
sudo docker build --no-cache -t samuelpinfo/emergentory-api:latest ./api
echo '----- Pusheando la API -----'
sudo docker push samuelpinfo/emergentory-api:latest

echo '----- Buildeando el Front -----'
sudo docker build --no-cache -t samuelpinfo/emergentory-front:latest ./front/
echo '----- Pusheando el Front -----'
sudo docker push samuelpinfo/emergentory-front:latest

echo '----- Las imágenes han sido buildeadas y pusheadas -----'
