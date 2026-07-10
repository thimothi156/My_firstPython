from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(20))
    addresses = relationship("Address")
    profile = relationship("UserProfile",uselist=False)
    order_items = relationship("OrderItem")
    products = relationship("Product",secondary="orderitems", back_populates="user")
    created_at = Column(DateTime(timezone = True),
                   server_default=func.now())
    updated_at = Column(DateTime(timezone = True),
                       server_default=func.now())

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer,primary_key=True, index=True)
    user_id = Column(ForeignKey('users.id'), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    user = relationship("User")
    created_at = Column(DateTime(timezone = True),
                   server_default=func.now())
    updated_at = Column(DateTime(timezone = True),
                       server_default=func.now())



class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    stock = Column(Integer)
    created_at = Column(DateTime(timezone = True),
                   server_default=func.now())
    updated_at = Column(DateTime(timezone = True),
                       server_default=func.now())
    category_id = Column(ForeignKey('categories.id'))
    category = relationship("Category")

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    parent_id = Column(ForeignKey("categories.id"))
    super_category = relationship("Category",
                     remote_side=[id],
                     backref="sub_categories")
    products = relationship("Product")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer,primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User")
    created_at = Column(DateTime(timezone = True),
           server_default=func.now())
    updated_at = Column(DateTime(timezone = True),
               server_default=func.now())

class OrderItem(Base):
    __tablename__ = "orderitems"
    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey("orders.id"))
    product_id = Column(ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Integer)
    order  = relationship("Order")
    product = relationship("Product")
    created_at = Column(DateTime(timezone = True),
           server_default=func.now())
    updated_at = Column(DateTime(timezone = True),
               server_default=func.now())

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True,)
    user_id = Column(ForeignKey("users.id"))
    city = Column(String(40))
    state = Column(String(100))
    country = Column(String(100))
    zip_code = Column(String(20))
    user = relationship("User")
    created_at = Column(DateTime(timezone = True),
           server_default=func.now())
    updated_at = Column(DateTime(timezone = True),
               server_default=func.now())

