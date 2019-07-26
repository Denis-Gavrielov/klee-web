FROM python:3.6

# install python tests
RUN pip install flake8
RUN pip install httpie

# install JS E2E tests
# RUN apt-get update && apt-get install -y sudo
# RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
# RUN sudo apt-get install -y nodejs
# TODO: in dockerize version, need to change these copy to new folder structure
COPY src/klee_web/ /titb/src/klee_web
COPY run_tests.sh /titb/
WORKDIR /titb/src/klee_web/tests
# RUN npm i puppeteer
# RUN npm install

# ## be able to launch docker
# # RUN apt --assume-yes install docker.io
RUN curl -sSL https://get.docker.com/ | sh
RUN apt install sudo

WORKDIR /titb
RUN pip install -r src/klee_web/requirements.txt

CMD /bin/bash src/klee_web/tests/run_tests.sh 
# CMD ["/bin/bash","source","src/klee_web/klee-web-environment.sh",";","source","run_tests.sh"]

# currently running with:
# sudo docker run --rm -it --network web_network -v /var/run/docker.sock:/var/run/docker.sock e2e_test /bin/bash
# sudo docker run --rm -it --network web_network -v /var/run/docker.sock:/var/run/docker.sock -v /tmp/:/tmp/ e2e_test /bin/bash

# possibly put this command into a file, which then is called by circle ci at the end of provisioning

# export OPENSSL_CONF=~/bin/etc/openssl.cnf
# this line helped with some issues

# the below solves the error.
# export OPENSSL_CONF=


# cd ../../../ && . src/klee_web/tests/run_tests.sh
