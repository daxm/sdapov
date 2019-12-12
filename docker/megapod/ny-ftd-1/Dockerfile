FROM dmickels/sdapov-baseimage:selfservelabs-latest
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Configure Script and GIT variables
ENV GIT_REPO https://github.com/daxm/sdapov.git
ENV GIT_BRANCH selfservelabs

ENV SCRIPT_PATH sdapov/docker/megapod/ny-ftd-1
ENV PYTHON_SCRIPT configure_ftd.py

ENV WORK_DIR /usr/src/app

WORKDIR $WORK_DIR

RUN git clone -b $GIT_BRANCH $GIT_REPO

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

CMD python3 $WORK_DIR/$SCRIPT_PATH/$PYTHON_SCRIPT
