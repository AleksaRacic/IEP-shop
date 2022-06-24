import json

from flask import Flask
from config import Config
from flask_migrate import Migrate, init, migrate, upgrade
from models import *
from sqlalchemy_utils import database_exists, create_database
from redis import Redis
from time import sleep
import json

application = Flask(__name__)
application.config.from_object(Config)

if __name__ == '__main__':

    database.init_app(application)
    with application.app_context() as context:
        with Redis(host=Config.REDIS_HOST) as redis:
            while True:
                bytesList = redis.lrange(Config.REDIS_THREADS_LIST, 0, 0)
                if len(bytesList) != 0:
                    bytes = redis.lpop(Config.REDIS_THREADS_LIST)
                    product_json = json.loads(bytes.decode("utf-8"))
                    product = Product.query.filter(Product.name == product_json['ime_proizvoda']).first()

                    if not product:
                        product = Product(
                            name=product_json['ime_proizvoda'],
                            price=product_json['cena'],
                            quantity=product_json['kolicina']
                        )
                        database.session.add(product)
                        database.session.commit()
                        categories = product_json['kategorije']
                        for category in categories:
                            db_category = Category.query.filter(Category.name == category).first()
                            if not db_category:
                                db_category = Category(name=category)
                                database.session.add(db_category)
                                database.session.commit()
                            productCategory = ProductCategory(productId=product.id, categoryId=db_category.id)
                            database.session.add(productCategory)
                            database.session.commit()

                    else:
                        category_list = product.categories

                        category_list = product.categories

                        categories = product_json['kategorije']
                        flag = True
                        for db_category in category_list:
                            if db_category.name not in categories:
                                flag = False
                                break
                        if flag:
                            new_quantity = product.quantity + product_json['kolicina']
                            new_price = (product.quantity * product.price + product_json['kolicina'] * product_json['cena'])/(new_quantity)
                            product.quantity = new_quantity
                            product.price = new_price
                            database.session.commit()

                    #proera narudzbi

                    pending_orders = Order.query.filter(Order.status == 'PENDING').order_by(Order.timestamp).all()

                    for order in pending_orders:
                        products = order.products
                        products = order.products

                        for product in products:
                            diff = product.requested - product.received
                            if diff > 0:
                                warehouse_product = Product.query.get(product.productId)

                                if warehouse_product.quantity >= diff:
                                    warehouse_product.quantity = warehouse_product.quantity - diff # ne skine quantity
                                    product.received += diff
                                    database.session.commit()
                                else:
                                    product.received += warehouse_product.quantity
                                    warehouse_product.quantity = 0
                                    database.session.commit()

                        flag = True

                        for product in products:
                            diff = product.requested - product.received
                            if diff > 0:
                                flag = False
                                break
                        if flag:
                            order.status = "COMPLETE"
                            database.session.commit()

                else:
                    print("sleeping")
                    sleep(5)
