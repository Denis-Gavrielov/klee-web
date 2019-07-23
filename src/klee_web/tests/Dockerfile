FROM python:3.6

# install python tests
RUN pip install flake8
RUN pip install httpie

# install JS E2E tests
RUN apt-get update && apt-get install -y sudo
RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
RUN sudo apt-get install -y nodejs
# TODO: in dockerize version, need to change these copy to new folder structure
COPY src/klee_web/ /titb/src/klee_web
COPY run_tests.sh /titb/
WORKDIR /titb/src/klee_web/tests
RUN npm install

WORKDIR /titb
RUN pip install -r src/klee_web/requirements.txt

CMD . src/klee_web/klee-web-environment.sh && . run_tests.sh
