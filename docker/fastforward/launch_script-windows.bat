
@echo off
SET DOCKER_IMAGE=dmickels/sdapov-fastforwardscripts:selfservelabs-latest
SET DOCKER_CONTAINER_NAME=fastforward
docker stop %DOCKER_CONTAINER_NAME%

@echo on
docker pull %DOCKER_IMAGE%
docker run -it --rm --name %DOCKER_CONTAINER_NAME% %DOCKER_IMAGE%

pause
