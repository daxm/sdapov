
@echo off
SET DOCKER_IMAGE=dmickels/sdapov-fastforwardscripts:dev
SET DOCKER_CONTAINER_NAME=fastforward
docker stop %DOCKER_CONTAINER_NAME%

@echo on
docker pull %DOCKER_IMAGE%
docker run --rm -it --name %DOCKER_CONTAINER_NAME% %DOCKER_IMAGE%

pause
