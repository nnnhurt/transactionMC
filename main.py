import os
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
from model.models import CustomerModel, ProductModel, OrderModel, OrderItemModel
from datetime import datetime

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)

def create_customer(session, first_name, last_name, email):
    """ Создание клиента перед заказом """
    try:
        new_customer = CustomerModel(first_name=first_name, last_name=last_name, email=email)
        session.add(new_customer)
        session.commit()
        print("Клиент успешно создан")
        return new_customer.customer_id
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")
        return None

def create_order(session, customer_id, items):
    """ Сценарий 1: Размещение заказа """
    try:
        customer = session.get(CustomerModel, customer_id)
        if not customer:
            raise ValueError(f"Клиент с ID {customer_id} не найден")

        new_order = OrderModel(customer_id=customer_id, order_date=datetime.utcnow(), total_amount=0.0)
        session.add(new_order)
        session.flush()
        
        total_amount = 0
        for item in items:
            product = session.get(ProductModel, item['product_id'])
            if not product:
                raise ValueError(f"Продукт с ID {item['product_id']} не найден")
            subtotal = product.price * item['quantity']
            total_amount += subtotal
            order_item = OrderItemModel(order_id=new_order.order_id, product_id=product.product_id, 
                                        quantity=item['quantity'], subtotal=subtotal)
            session.add(order_item)
        
        new_order.total_amount = total_amount
        session.commit()
        print("Заказ успешно создан")
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")

def update_customer_email(session, customer_id, new_email):
    """ Сценарий 2: Обновление email клиента """
    try:
        stmt = update(CustomerModel).where(CustomerModel.customer_id == customer_id).values(email=new_email)
        session.execute(stmt)
        session.commit()
        print("Email клиента успешно обновлен")
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")

def add_product(session, product_name, price):
    """ Сценарий 3: Добавление продукта """
    try:
        new_product = ProductModel(product_name=product_name, price=price)
        session.add(new_product)
        session.commit()
        print("Продукт успешно добавлен")
    except Exception as e:
        session.rollback()
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    session = SessionLocal()
    
    customer_id = create_customer(session, "Иван", "Иванов", "ivan@example.com")
    if customer_id:
        create_order(session, customer_id=customer_id, items=[
            {'product_id': 1, 'quantity': 2},
            {'product_id': 2, 'quantity': 1}
        ])
    
    update_customer_email(session, customer_id=customer_id, new_email="newemail@example.com")
    
    add_product(session, product_name="Новый товар", price=99.99)
    
    session.close()
