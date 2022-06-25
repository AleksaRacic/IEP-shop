FROM python:3

RUN mkdir -p /opt/src/deamon
WORKDIR /opt/src/deamon

COPY ProdavnicaApps/Deamon/app.py ./app.py
COPY ProdavnicaApps/Deamon/config.py ./config.py
COPY ProdavnicaApps/Deamon/models.py ./models.py

COPY ProdavnicaApps/Deamon/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/customer"

ENTRYPOINT ["python", "./app.py"]