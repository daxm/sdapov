FROM dmickels/sdapov-baseimage:latest
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Configure Script and GIT variables
ENV PYTHON_SCRIPT configure_fmc.py
ENV GIT_REPO https://github.com/daxm/sdapov.git
ENV GIT_BRANCH selfservelabs
ENV SCRIPT_PATH sdapov/docker/fmc_config

WORKDIR /usr/src/app

RUN git clone -b $GIT_BRANCH $GIT_REPO

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/$SCRIPT_PATH
CMD python3 $PYTHON_SCRIPT
