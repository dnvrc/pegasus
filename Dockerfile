FROM python:3.6.6-slim

RUN apt-get update -y && apt-get install -y \
    apt-transport-https \
    build-essential \
    ca-certificates \
    git-core \
    gnupg2 \
    graphviz \
    libffi6 \
    libffi-dev \
    libgdbm-dev \
    libglu1-mesa-dev \
    lsb-release \
    make \
    python-dev \
    python-pydot \
    python-pydot-ng \
    python3-gdbm \
    python3-gdbm-dbg \
    software-properties-common

WORKDIR /opt/app
ADD . /opt/app
RUN make docker_install
