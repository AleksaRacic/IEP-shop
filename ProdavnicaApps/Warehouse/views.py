import json
import csv
from time import sleep

from redis import Redis
from utils import roleCheck

from flask import Blueprint
from flask import request, Response

from config import Config
warehouse_view = Blueprint('warehouse_view', __name__)


@warehouse_view.route("/update", methods=["POST"])
@roleCheck('Worker')
def register():
    #TODO uvesti proveru da mora biti magacioner
    file = request.files.get('file', None)

    if not file:
        return Response(json.dumps({
            'message': 'Field file is missing.'
        }), status=400)

    csv_string = file.read().decode('utf-8')
    lines = csv_string.splitlines()
    csvreader = csv.reader(lines)
    products = []
    counter = 0
    for row in csvreader:
        if len(row) != 4:
            return Response(json.dumps({
                'message': f'Incorrect number of values on line {counter}.'
            }), status=400)
        kategorije = row[0].split('|')
        ime_proizvoda = row[1]
        try:
            kolicina = int(row[2])
        except Exception:
            return Response(json.dumps({
                'message': f'Incorrect quantity on line {counter}.'
            }), status=400)
        if kolicina <= 0:
            return Response(json.dumps({
                'message': f'Incorrect quantity on line {counter}.'
            }), status=400)
        try:
            cena = float(row[3])
        except Exception:
            return Response(json.dumps({
                'message': f'Incorrect price on line {counter}.'
            }), status=400)

        if cena <= 0:
            return Response(json.dumps({
                'message': f'Incorrect price on line {counter}.'
            }), status=400)

        products.append({
            'kategorije' : kategorije,
            'ime_proizvoda' : ime_proizvoda,
            'kolicina' : kolicina,
            'cena' : cena
        })
        counter += 1

    with Redis(host=Config.REDIS_HOST) as redis:
        for product in products:
            redis.rpush(Config.REDIS_THREADS_LIST, json.dumps(product))
    return Response(status=200)


