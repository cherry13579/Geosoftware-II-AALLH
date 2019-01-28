@echo off
cd MapSearch
start cmd /k python webmap.py
cd ..
cd pycsw
docker stop aahll-pycsw
docker rm aahll-pycsw 
start powershell -noexit -command docker run --name aahll-pycsw --volume ${PWD}/pycsw:/usr/lib/python3.5/site-packages/pycsw --volume ${PWD}/docs:/home/pycsw/docs --volume ${PWD}/VERSION.txt:/home/pycsw/VERSION.txt --volume ${PWD}/LICENSE.txt:/home/pycsw/LICENSE.txt --volume ${PWD}/COMMITTERS.txt:/home/pycsw/COMMITTERS.txt --volume ${PWD}/CONTRIBUTING.rst:/home/pycsw/CONTRIBUTING.rst --volume ${PWD}/pycsw/plugins:/home/pycsw/pycsw/plugins --volume ${PWD}/aahll.cfg:/etc/pycsw/pycsw.cfg --volume ${PWD}/db-data:/home/pycsw/db-data/ --publish 8000:8000 aahll-pycsw --reload