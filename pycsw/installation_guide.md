# Installation guide for A²HL²-pycsw #

## Install from Code - Setting up a development environment with docker ##

- install docker: [https://docs.docker.com/install/](https://docs.docker.com/install/)
- clone our repository to your computer
- make sure, docker is running
- open Windows PowerShell (or Docker Toolbox) on your computer and navigate into the pycsw folder: 

```
cd .../pycsw
```

- add the following in PowerShell (just completely copy and paste):

```
docker run --name pycsw-dev --volume ${PWD}/pycsw:/usr/lib/python3.5/site-packages/pycsw --volume ${PWD}/docs:/home/pycsw/docs --volume ${PWD}/VERSION.txt:/home/pycsw/VERSION.txt --volume ${PWD}/LICENSE.txt:/home/pycsw/LICENSE.txt --volume ${PWD}/COMMITTERS.txt:/home/pycsw/COMMITTERS.txt --volume ${PWD}/CONTRIBUTING.rst:/home/pycsw/CONTRIBUTING.rst --volume ${PWD}/pycsw/plugins:/home/pycsw/pycsw/plugins --volume ${PWD}/our.cfg:/etc/pycsw/pycsw.cfg --volume ${PWD}/db-data:/db-data/ --publish 8000:8000 geopython/pycsw --reload
```

- sometimes you could get an input/output error, if so, simply restart Docker and try again
- go to localhost:8000 in your browser, when you see a xml tree, everething went fine
- to remove the container, add the following in powerShell (necessary if the container should be restarted with the above command):

```
docker rm -f pycsw-dev
```

## Run image from docker-hub ##