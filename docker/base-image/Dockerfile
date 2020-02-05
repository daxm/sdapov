FROM ubuntu:18.04
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Running APT UPDATE
RUN apt-get -y update

# Install APT-UTILS
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils locales

# Running APT DIST-UPGRADE
RUN apt-get -y dist-upgrade

# Running APT AUTOREMOVE
RUN apt-get -y autoremove

# Running APT AUTOCLEAN
RUN apt-get -y autoclean

# Install Python modules
RUN apt-get -y install python3 python3-pip

# Install get
RUN apt-get install -y git
