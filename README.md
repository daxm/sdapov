# SDA PoV Repo
Though there is only a "docker" folder in this repo at the moment the idea is to use this repository to hold/contain
public facing information that could be useful for running a Cisco SDA PoV.

## Docker
In the docker folder there are 3 different projects:  base-image, fastforward, and fmc_config.  Each have their own
Dockerfile files and purposes.

### base-image
This is the initial Docker image that the other projects (fastforward and fmc_config) will pull from.  The idea is that
we could add new content to the base-image and it would automatically become available to the other projects.

### fastforward
This Docker image is used to run a Python script that uses source Postman files to configure Cisco DNAC via its API.

### fmc_config
This Docker image is used to run a Python script that uses the fmcapi Python package to configure Cisco FMC/FTD via its API.

