import os
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from model.meta import Base



class CustomerModel(Base):
    __tablename__ = "customer"
    
    customer_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

class ProductModel(Base):
    __tablename__ = "product"
    
    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

class OrderModel(Base):
    __tablename__ = "order"
    
    order_id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey('customer.customer_id'), nullable=False)
    customer: Mapped['CustomerModel'] = relationship(backref='order')
    order_date: Mapped[datetime] = mapped_column(nullable=False)
    total_amount: Mapped[float] = mapped_column(nullable=False)

class OrderItemModel(Base):
    __tablename__ = "order_item"
    
    order_item_id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('order.order_id'), nullable=False)
    order: Mapped['OrderModel'] = relationship(backref='order_item')
    product_id: Mapped[int] = mapped_column(ForeignKey('product.product_id'), nullable=False)
    product: Mapped['ProductModel'] = relationship(backref='order_item')
    quantity: Mapped[int] = mapped_column(nullable=False)
    subtotal: Mapped[float] = mapped_column(nullable=False)
