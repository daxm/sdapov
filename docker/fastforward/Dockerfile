FROM dmickels/sdapov-baseimage:selfservelabs-latest
MAINTAINER Dax Mickelson (dmickels@cisco.com)

# Configure Script and GIT variables
ENV PYTHON_SCRIPT sdapovfastforward.py
ENV GIT_REPO https://github.com/ankanani/sdapovfastforward.git
ENV GIT_BRANCH selfservelabs
ENV SCRIPT_PATH sdapovfastforward

WORKDIR /usr/src/app

RUN git clone $GIT_REPO
#RUN git checkout $GIT_BRANCH

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/$SCRIPT_PATH

CMD python3 $PYTHON_SCRIPT
