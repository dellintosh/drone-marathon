FROM python:3.5.1-alpine

WORKDIR /usr/src/app/

ADD requirements.txt /tmp/

RUN apk --no-cache add --virtual .build-dependencies ca-certificates \
  && apk --no-cache add --virtual .run-dependencies python py-pip \
  && pip install -r /tmp/requirements.txt \
  && rm /tmp/requirements.txt \
  && apk del .build-dependencies

ADD run_marathon.py /usr/bin/

ENTRYPOINT ["python3", "/usr/bin/run_marathon.py"]
