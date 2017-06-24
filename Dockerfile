FROM python:3.5-alpine
LABEL maintainer ECG Engineering <techalerts@expansioncapitalgroup.com>

ENV PYTHONPATH /run/app

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY manage.py /run/manage.py
COPY app /run/app

ENTRYPOINT ["python", "/run/manage.py"]
