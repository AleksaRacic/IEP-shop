import datetime
import json
from sqlalchemy import and_, func

from flask import Blueprint
from flask import request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import *
from utils import roleCheck

admin_view = Blueprint('admin_view', __name__)


@admin_view.route("/productStatistics", methods=["GET"])
@roleCheck('Admin')
def productStatistics():
    products = Product.query.all()
    statistics = []
    for product in products:
        requested = 0
        received = 0

        sales = product.sales
        sales = product.sales
        for sale in sales:
            requested += sale.requested
            received += sale.received
        if requested == 0:
            continue
        statistics.append({
            'name': product.name,
            'sold' : requested,
            'waiting' : requested - received
        }
        )

    return Response(json.dumps(
        {
            'statistics' : statistics
        }
    ), status=200)

@admin_view.route("/categoryStatistics", methods=["GET"])
@roleCheck('Admin')
def categoryStatistics():
    sa_prodajom = database.session.query(
        Category.name,
        func.sum(ProductOrder.requested).label("sum")
    ).filter(and_(
        Product.id == ProductCategory.productId,
        Category.id == ProductCategory.categoryId))\
    .filter(
        Product.id == ProductOrder.productId
    ).group_by(Category.name).order_by(func.sum(ProductOrder.requested).desc(), Category.name).all()
    #naknadno dodati ostale kategorije

    sve_zajedno = Category.query.order_by(Category.name).all()

    statistics = [i.name for i in sa_prodajom]
    sve = [cat.name for cat in sve_zajedno]

    for s in sve:
        if s not in statistics:
            statistics.append(s)

    return Response(json.dumps(
        {
            'statistics': statistics
        }
    ), status=200)