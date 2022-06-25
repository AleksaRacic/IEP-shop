FROM python:3

RUN mkdir -p /opt/src/prodavnica
WORKDIR /opt/src/prodavnica

COPY ProdavnicaApps/Deamon/migrate.py ./migrate.py
COPY ProdavnicaApps/Deamon/config.py ./config.py
COPY ProdavnicaApps/Deamon/models.py ./models.py

COPY ProdavnicaApps/Deamon/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/prodavnica"

ENTRYPOINT ["python", "./migrate.py"]