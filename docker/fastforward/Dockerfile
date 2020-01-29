FROM dmickels/sdapov-baseimage:dnacentersdk
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Configure Script and GIT variables
ENV CODE_REPO https://github.com/daxm/sdapov.git
ENV GIT_BRANCH dnacentersdk
ENV WORK_DIR /usr/src/app
ENV SCRIPT_PATH $WORK_DIR/sdapov/docker/fastforward
ENV PYTHON_SCRIPT bootstrap.py

# Clone repos.
WORKDIR $WORK_DIR
RUN git clone -b $GIT_BRANCH $CODE_REPO

# Install Python modules needed for this script.
RUN python3 -m pip install --no-cache-dir -r $SCRIPT_PATH/requirements.txt

# Run script.
WORKDIR $SCRIPT_PATH
CMD python3 $SCRIPT_PATH/$PYTHON_SCRIPT