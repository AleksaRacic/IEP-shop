FROM python:3

RUN mkdir -p /opt/src/warehouse
WORKDIR /opt/src/warehouse

COPY ProdavnicaApps/Warehouse/app.py ./app.py
COPY ProdavnicaApps/Warehouse/config.py ./config.py
COPY ProdavnicaApps/Warehouse/utils.py ./utils.py
COPY ProdavnicaApps/Warehouse/views.py ./views.py

COPY ProdavnicaApps/Warehouse/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/warehouse"

ENTRYPOINT ["python", "./app.py"]