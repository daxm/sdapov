FROM ubuntu:18.04
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Running APT UPDATE
RUN apt-get -y update

# Install APT-UTILS
RUN apt-get install -y apt-utils

# Running APT DIST-UPGRADE
RUN apt-get -y dist-upgrade

# Running APT AUTOREMOVE
RUN apt-get -y autoremove

# Running APT AUTOCLEAN
RUN apt-get -y autoclean

# Install Python modules
RUN apt-get -y install python3 python3-pip

# Install node.js
RUN apt-get install -y nodejs

# Install npm
RUN apt-get install -y npm

# Install newman
RUN npm install -g newman

# Install get
RUN apt-get install -y git
