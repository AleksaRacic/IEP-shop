FROM python:3

RUN mkdir -p /opt/src/auth
WORKDIR /opt/src/auth

COPY Auth/app.py ./app.py
COPY Auth/config.py ./config.py
COPY Auth/models.py ./models.py
COPY Auth/utils.py ./utils.py
COPY Auth/views.py ./views.py

COPY Auth/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/auth"

ENTRYPOINT ["python", "./app.py"]