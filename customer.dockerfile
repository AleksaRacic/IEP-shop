FROM python:3

RUN mkdir -p /opt/src/customer
WORKDIR /opt/src/customer

COPY ProdavnicaApps/Customer/app.py ./app.py
COPY ProdavnicaApps/Customer/config.py ./config.py
COPY ProdavnicaApps/Customer/models.py ./models.py
COPY ProdavnicaApps/Customer/utils.py ./utils.py
COPY ProdavnicaApps/Customer/views.py ./views.py

COPY ProdavnicaApps/Customer/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/customer"

ENTRYPOINT ["python", "./app.py"]