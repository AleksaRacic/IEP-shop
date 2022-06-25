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
    while True:
        with application.app_context() as context:
            with Redis(host=Config.REDIS_HOST) as redis:

                bytes = redis.lpop(Config.REDIS_THREADS_LIST) #mozda da stalno popuje, brze ce biti
                if bytes:
                    product_json = json.loads(bytes.decode("utf-8"))
                    product = Product.query.filter(Product.name == product_json['ime_proizvoda']).first()
                    if not product:
                        print('ime', product_json['ime_proizvoda'])
                        product = Product(
                            name=product_json['ime_proizvoda'],
                            price=product_json['cena'],
                            quantity=product_json['kolicina']
                        )
                        database.session.add(product)
                        database.session.commit()
                        print('kolicina', product.quantity)
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
                        print('ime', product_json['ime_proizvoda'])
                        print('tmp0',product.quantity)
                        category_list = product.categories

                        category_list = product.categories

                        categories = product_json['kategorije']
                        flag = True
                        for db_category in category_list:
                            if db_category.name not in categories:
                                flag = False
                                break

                        if flag:
                            old_quantity = product.quantity

                            print('oq', old_quantity)
                            print('kolicina', product_json['kolicina'])

                            new_quantity = old_quantity + product_json['kolicina']
                            new_price = (product.quantity * product.price + product_json['kolicina'] * product_json['cena'])/( new_quantity )

                            print('nq', new_quantity)
                            print('np', new_price)

                            product.price = new_price
                            if old_quantity == 0:
                                pending_orders = Order.query.filter(Order.status == 'PENDING').order_by(Order.timestamp).all()

                                break_ = False

                                for order in pending_orders:
                                    products = order.products
                                    products = order.products

                                    for order_product in products:
                                        if order_product.productId == product.id:
                                            need = order_product.requested - order_product.received
                                            if need == 0:
                                                continue
                                            print('need', need)
                                            print('received', order_product.received)
                                            print('nq2', new_quantity)
                                            order_product.received = order_product.received + min(need, new_quantity)
                                            new_quantity = max(new_quantity - need, 0)
                                            print('nq3', new_quantity)

                                            if new_quantity == 0:
                                                break_ = True
                                                break
                                    if break_ :
                                        break

                                product.quantity = new_quantity
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
                                product.quantity = new_quantity
                                database.session.commit()
                else:
                    pass
                    #sleep(5)
