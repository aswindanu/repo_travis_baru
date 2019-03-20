#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /home/ubuntu/repo_travis_baru &&
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | sudo docker login --username $DOCKERHUB_USER --password-stdin
sudo docker stop hello4
sudo docker rm hello4
sudo docker rmi blasterb0y/hello4
sudo docker run -d --name hello4 -p 5000:5000 blasterb0y/hello4:latest
