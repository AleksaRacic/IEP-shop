from flask import Flask
from config import Config
from flask_migrate import Migrate, init, migrate, upgrade
from sqlalchemy_utils import database_exists, create_database
from models import *

application = Flask(__name__)
application.config.from_object(Config)

migrateObject = Migrate(application, database)

if (not database_exists(application.config["SQLALCHEMY_DATABASE_URI"])):
    create_database(application.config["SQLALCHEMY_DATABASE_URI"])

database.init_app(application)

with application.app_context() as context:
    init()
    migrate(message="Production migration")
    upgrade()

    category1 = Category(name='Category1')
    category2 = Category(name='Category2')
    category3 = Category(name='Category3')
    category4 = Category(name='Category4')

    database.session.add(category1)
    database.session.add(category2)
    database.session.add(category3)
    database.session.add(category4)

    product1 = Product(
        name="Product1",
        price=4.6,
        quantity=2
    )

    product2 = Product(
        name="Product2",
        price=44.6,
        quantity=32
    )
    product3 = Product(
        name="Product3",
        price=2.6,
        quantity=12
    )

    database.session.add(product1)
    database.session.add(product2)
    database.session.add(product3)

    database.session.commit()

    database.session.add(ProductCategory(productId=product1.id, categoryId=category1.id))
    database.session.add(ProductCategory(productId=product1.id, categoryId=category2.id))
    database.session.add(ProductCategory(productId=product2.id, categoryId=category3.id))
    database.session.add(ProductCategory(productId=product2.id, categoryId=category1.id))
    database.session.add(ProductCategory(productId=product3.id, categoryId=category4.id))
    database.session.add(ProductCategory(productId=product3.id, categoryId=category1.id))
    database.session.add(ProductCategory(productId=product3.id, categoryId=category2.id))

    database.session.commit()








