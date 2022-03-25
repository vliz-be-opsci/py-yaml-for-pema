FROM python:3.8-buster

COPY ./ /yaml4parms
WORKDIR /yaml4parms

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python setup.py install

ENTRYPOINT ["yaml4parms"]
