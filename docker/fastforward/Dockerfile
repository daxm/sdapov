FROM dmickels/sdapov-baseimage:selfservelabs-latest
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Configure Script and GIT variables
ENV CODE_REPO https://github.com/daxm/sdapov.git
ENV POSTMAN_REPO https://github.com/ankanani/sdapovfastforward-postman
ENV GIT_BRANCH selfservelabs
ENV WORK_DIR /usr/src/app
ENV SCRIPT_PATH $WORK_DIR/sdapov/docker/fastforward
ENV PYTHON_SCRIPT sdapovfastforward.py

# Clone repos.
WORKDIR $WORK_DIR
RUN git clone -b $GIT_BRANCH $CODE_REPO
RUN git clone -b $GIT_BRANCH $POSTMAN_REPO

# Install Python modules needed for this script.
RUN python3 -m pip install --no-cache-dir -r $SCRIPT_PATH/requirements.txt

# Run script.
WORKDIR $SCRIPT_PATH
CMD python3 $PYTHON_SCRIPT
