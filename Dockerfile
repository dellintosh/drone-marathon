# Deploys to a Marathon cluster
#
#     docker build --rm=true -t expansioncap/drone-marathon .

FROM gliderlabs/alpine:3.2
MAINTAINER Justus Luthy <jluthy@expansioncapitalgroup.com>

RUN apk-install python3 bash
#RUN mkdir -p /tmp/drone-marathon

#COPY requirements.txt /tmp/drone-marathon/
#RUN pip3 install -r /tmp/drone-marathon/requirements.txt
#WORKDIR /tmp/drone-marathon

ADD ./ /tmp/drone-marathon
RUN cd /tmp/drone-marathon \
    && pip3 install -r requirements.txt \
    && python3 setup.py install \
    && rm -rf /tmp/drone-marathon

ENTRYPOINT ["drone-marathon"]
