FROM python:3

RUN mkdir -p /opt/src/admin
WORKDIR /opt/src/admin

COPY ProdavnicaApps/Admin/app.py ./app.py
COPY ProdavnicaApps/Admin/config.py ./config.py
COPY ProdavnicaApps/Admin/models.py ./models.py
COPY ProdavnicaApps/Admin/utils.py ./utils.py
COPY ProdavnicaApps/Admin/views.py ./views.py

COPY ProdavnicaApps/Admin/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/admin"

ENTRYPOINT ["python", "./app.py"]