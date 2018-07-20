FROM python/python-base-image:3.6-slim

RUN apt-get update -y && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    gnupg2 \
    libffi6 \
    libffi-dev \
    libgdbm-dev \
    libglu1-mesa-dev \
    lsb-release \
    python-dev \
    python3-gdbm \
    python3-gdbm-dbg \
    software-properties-common

WORKDIR /opt/app
ADD . /opt/app
RUN make docker_install
