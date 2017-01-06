FROM python:3.5.1-alpine

RUN apk add -U \
    ca-certificates \
 && rm -rf /var/cache/apk/* \
 && pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel

WORKDIR /usr/src/app/
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --use-wheel --no-index -r requirements.txt
ADD run_marathon.py /usr/bin/

ENTRYPOINT ["python3", "/usr/bin/run_marathon.py"]
