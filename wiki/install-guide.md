# Installing Docker and BrewPi on Ubuntu

We'll install Docker to run BrewPi in a container. This keeps it nicely isolated from the rest of the system and makes it easy to deploy.

## Install Docker

Install docker following these instructions:

https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/

Install docker-compose:

```
sudo apt install python-pip
pip install --user docker-compose
```

## Deploy the containers

Copy this code to a file called `docker-compose.yml`

```yml
version: '3'

services:
  brewpi:
    image: brewpi/brewpi-ubuntu
    restart: always
    privileged: true
    volumes:
      - ~/brewpi-data:/data
      - /etc/timezone:/etc/timezone
      - /etc/localtime:/etc/localtime
    ports:
      - "80:80"

  portainer:
    image: portainer/portainer
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    ports:
      - "9000:9000"
```

Open a terminal in the directory where you saved the file, and run the following command to get started:

```
docker-compose up
```

