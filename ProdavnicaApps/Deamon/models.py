from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class ProductOrder(database.Model):
    __tablename__ = "productOrder"

    id = database.Column(database.Integer, primary_key=True)
    productId = database.Column(database.Integer, database.ForeignKey("products.id"), nullable=False)
    orderId = database.Column(database.Integer, database.ForeignKey("orders.id"), nullable=False)

    price = database.Column(database.Float, nullable=False)
    received = database.Column(database.Integer, nullable=False)
    requested = database.Column(database.Integer, nullable=False)


class ProductCategory(database.Model):
    __tablename__ = "productcategory"

    id = database.Column(database.Integer, primary_key=True)
    productId = database.Column(database.Integer, database.ForeignKey("products.id"), nullable=False)
    categoryId = database.Column(database.Integer, database.ForeignKey("categories.id"), nullable=False)


class Product(database.Model):
    __tablename__ = "products"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)
    quantity = database.Column(database.Integer, nullable=False)
    price = database.Column(database.Float, nullable=False)
    categories = database.relationship("Category", secondary=ProductCategory.__table__, back_populates="products")
    sales = database.relationship("ProductOrder")


class Category(database.Model):
    __tablename__ = "categories"

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(256), nullable=False)
    products = database.relationship("Product", secondary=ProductCategory.__table__, back_populates="categories")

class Order(database.Model):
    __tablename__ = "orders"

    id = database.Column(database.Integer, primary_key=True)
    timestamp = database.Column(database.DateTime, nullable=False)
    price = database.Column(database.Float, nullable=False)
    status = database.Column(database.String(256), nullable=False)
    products = database.relationship("ProductOrder")
    email = database.Column(database.String(256), nullable=False)


