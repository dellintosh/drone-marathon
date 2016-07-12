# Deploys to a Marathon cluster
#
#     docker build --rm=true -t expansioncap/drone-marathon .

FROM gliderlabs/alpine:3.2
MAINTAINER Justus Luthy <jluthy@expansioncapitalgroup.com>

RUN apk-install python3 bash
RUN mkdir -p /tmp/drone-marathon

COPY requirements.txt /tmp/drone-marathon/
RUN pip3 install -r /tmp/drone-marathon/requirements.txt
#WORKDIR /tmp/drone-marathon

COPY plugin /tmp/drone-marathon/
RUN python3 setup.py install

#ENTRYPOINT ["bash"]
#ENTRYPOINT ["python3", "/plugin/main.py"]
ENTRYPOINT ["drone-marathon"]
