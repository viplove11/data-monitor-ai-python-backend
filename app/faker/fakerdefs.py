import psycopg2
from psycopg2.extras import execute_values
from faker import Faker
import uuid
import random


NUM_USERS = 1000
NUM_STORES = 50
NUM_PRODUCTS = 500
NUM_ORDERS = 5000
NUM_ORDER_ITEMS = 15000

fake = Faker()

def setup_schema(cur : psycopg2.extensions.cursor):
    cur.execute("""
            DROP TABLE IF EXISTS order_items, orders, products, stores, users CASCADE;
            CREATE TABLE users (
                id UUID PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(50), -- Nullable
                created_at TIMESTAMP NOT NULL
            );
            CREATE TABLE stores (
                id UUID PRIMARY KEY,
                store_name VARCHAR(100) NOT NULL,
                region VARCHAR(100) -- Nullable
            );
            CREATE TABLE products (
                id UUID PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                description TEXT -- Nullable
            );
            CREATE TABLE orders (
                id UUID PRIMARY KEY,
                user_id UUID NOT NULL REFERENCES users(id),
                store_id UUID REFERENCES stores(id), -- Nullable (e.g., online order)
                order_date TIMESTAMP NOT NULL,
                status VARCHAR(50) NOT NULL
            );
            CREATE TABLE order_items (
                id UUID PRIMARY KEY,
                order_id UUID NOT NULL REFERENCES orders(id),
                product_id UUID NOT NULL REFERENCES products(id),
                quantity INT NOT NULL,
                discount_applied DECIMAL(5, 2) -- Nullable
            );
        """)

def generate_data(cur : psycopg2.extensions.cursor):
    users = [(
        str(uuid.uuid4()),
        fake.user_name(),
        fake.unique.email(),
        fake.phone_number() if random.random() > 0.3 else None,
        fake.date_time_this_decade()
    ) for _ in range(NUM_USERS)]
    stores = [(
        str(uuid.uuid4()),
        fake.company(),
        fake.city() if random.random() > 0.2 else None
    ) for _ in range(NUM_STORES)]

    products = [(
        str(uuid.uuid4()),
        fake.catch_phrase(),
        round(random.uniform(5.0, 500.0), 2),
        fake.text() if random.random() > 0.5 else None
    ) for _ in range(NUM_PRODUCTS)]

    user_ids = [u[0] for u in users]
    store_ids = [s[0] for s in stores]
    product_ids = [p[0] for p in products]

    orders = [(
        str(uuid.uuid4()),
        random.choice(user_ids),
        random.choice(store_ids) if random.random() > 0.4 else None,
        fake.date_time_between(start_date='-2y', end_date='now'),
        random.choice(['PENDING', 'SHIPPED', 'DELIVERED', 'CANCELLED'])
    ) for _ in range(NUM_ORDERS)]

    order_ids = [o[0] for o in orders]

    order_items = [(
        str(uuid.uuid4()),
        random.choice(order_ids),
        random.choice(product_ids),
        random.randint(1, 10),
        round(random.uniform(0.05, 0.50), 2) if random.random() > 0.7 else None
    ) for _ in range(NUM_ORDER_ITEMS)]

    execute_values(cur, "INSERT INTO users (id, username, email, phone, created_at) VALUES %s", users, page_size=1000)
    execute_values(cur, "INSERT INTO stores (id, store_name, region) VALUES %s", stores, page_size=1000)
    execute_values(cur, "INSERT INTO products (id, name, price, description) VALUES %s", products, page_size=1000)
    execute_values(cur, "INSERT INTO orders (id, user_id, store_id, order_date, status) VALUES %s", orders, page_size=1000)
    execute_values(cur, "INSERT INTO order_items (id, order_id, product_id, quantity, discount_applied) VALUES %s", order_items, page_size=1000)
