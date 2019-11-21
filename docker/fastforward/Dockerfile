FROM dmickels/sdapov-baseimage:selfservelabs-latest
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Configure Script and GIT variables
ENV PYTHON_SCRIPT sdapovfastforward.py
ENV CODE_REPO https://github.com/daxm/sdapov.git
ENV POSTMAN_REPO https://github.com/ankanani/sdapovfastforward-postman
ENV GIT_BRANCH selfservelabs
ENV SCRIPT_PATH sdapov/docker/fastforward

WORKDIR /usr/src/app

RUN git clone -b $GIT_BRANCH $CODE_REPO
RUN git clone -b $GIT_BRANCH $POSTMAN_REPO

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/$SCRIPT_PATH
CMD python3 $PYTHON_SCRIPT
