FROM e20co/python:3.5
LABEL maintainer ECG Engineering <techalerts@expansioncapitalgroup.com>

ENV PYTHONPATH /run/app

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY manage.py /run/manage.py
COPY app /run/app

ENTRYPOINT ["python", "/run/manage.py"]

# FROM python:3.5.1-alpine
#
# WORKDIR /app
#
# ADD requirements.txt /tmp/
#
# RUN apk --no-cache add --virtual .build-dependencies ca-certificates \
#   && apk --no-cache add --virtual .run-dependencies python py-pip \
#   && pip install -r /tmp/requirements.txt \
#   && rm /tmp/requirements.txt \
#   && apk del .build-dependencies
#
# ADD app /app
#
# ENTRYPOINT ["python3", "/app/run.py"]
