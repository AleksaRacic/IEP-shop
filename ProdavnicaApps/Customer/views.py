import datetime
import json
import re
from sqlalchemy import and_

from flask import Blueprint
from flask import request, Response, jsonify
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, get_jwt, \
    get_jwt_identity
from models import *

customer_view = Blueprint('customer_view', __name__)


# TODO dodaj jwt
@customer_view.route("/search", methods=["GET"])
@jwt_required()
def search():
    name = request.args.get('name')
    category = request.args.get('category')
    initial_querry = database.session.query(
        Product,
        ProductCategory,
        Category
    ).filter(and_(Product.id == ProductCategory.productId, Category.id == ProductCategory.categoryId))

    if name:
        initial_querry = initial_querry.filter(Product.name.contains(name))

    if category:
        initial_querry = initial_querry.filter(Category.name.contains(category))

    results = initial_querry.all()
    result_categories = []
    result_products = []
    control_products = []

    for result in results:
        cat = result.Category.name
        prod = result.Product
        if cat not in result_categories:
            result_categories.append(cat)
        product_cat = prod.categories #prefetch
        product_cat = prod.categories
        if prod.name not in control_products:
            product = {
                'categories' : [
                    p.name for p in product_cat
                ],
                'id' : prod.id,
                'name' : prod.name,
                'price' : prod.price,
                'quantity' : prod.quantity
            }
            result_products.append(product)
            control_products.append(prod.name)

    return Response(json.dumps(
        {
            'categories': result_categories,
            'products': result_products
        }
    ), status=200)


@customer_view.route("/order", methods=["POST"])
@jwt_required()
def order():
    identity = get_jwt_identity()
    req = request.json.get('requests', None)
    if not req:
        return Response(json.dumps({
            'message': 'Field request is missing.'
        }), status=400)

    count = 0

    wanted_products = []

    for r in req:
        id = r.get('id', None)
        if not id:
            return Response(json.dumps({
                'message': f'Product id is missing for request number {count}.'
            }), status=400)

        quantity = r.get('quantity', None)
        if not quantity:
            return Response(json.dumps({
                'message': f'Product quantity is missing for request number {count}.'
            }), status=400)

        try:
            id = int(id)
        except Exception:
            return Response(json.dumps({
                'message': f'Incorrect product id for request number {count}.'
            }), status=400)
        if id < 0:
            return Response(json.dumps({
                'message': f'Incorrect product id for request number{count}.'
            }), status=400)

        try:
            quantity = int(quantity)
        except Exception:
            return Response(json.dumps({
                'message': f'Incorrect product quantity for request number {count}.'
            }), status=400)
        if quantity <= 0:
            return Response(json.dumps({
                'message': f'Incorrect product quantity for request number{count}.'
            }), status=400)

        product = Product.query.get(id)

        if not product:
            return Response(json.dumps({
                'message': f'Incorrect product quantity for request number{count}.'
            }), status=400)

        wanted_products.append([product, quantity])

    order = Order(timestamp=datetime.datetime.now(), price = 0.0, status = "open", email=identity)
    database.session.add(order)

    completed = True
    price = 0.0
    for wanted_product in wanted_products:
        product = wanted_product[0]
        quantity = wanted_product[1]
        if product.quantity >= quantity:
            received = quantity
            product.quantity = product.quantity - quantity
            database.session.commit()
        else:
            received = product.quantity
            product.quantity = 0
            database.session.commit()
            completed = False
        price += quantity * product.price

        product_order = ProductOrder(
            productId=product.id,
            orderId=order.id,
            price=product.price,
            received=received,
            requested=quantity
        )
        database.session.add(product_order)
    order.price = price
    if completed:
        order.status = 'COMPLETE'
    else:
        order.status = 'PENDING'
    database.session.commit()

    return Response(json.dumps({
        'id' : order.id
    }), status=200)

@customer_view.route("/status", methods=["GET"])
@jwt_required()
def satus():
    identity = get_jwt_identity()
    orders = Order.query.filter(Order.email == identity)

    orders_list = []
    for order in orders:
        products_list = []
        products = order.products
        products = order.products
        for product in products:
            product_warehouse = Product.query.get(product.productId)
            categories = product_warehouse.categories
            categories = product_warehouse.categories
            categories_list = [cat.name for cat in categories]
            products_list.append({
                'categories' : categories_list,
                'name' : product_warehouse.name,
                'price' : product.price,
                'received' : product.received,
                'requested' : product.requested
            })
        orders_list.append(
            {
                'products': products_list,
                'price' : order.price,
                'status' : order.status,
                'timestamp' : order.timestamp.isoformat()
            }
        )

    return Response(json.dumps({
        'orders': orders_list
    }), status=200)
