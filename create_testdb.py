import os
import mysql.connector
import random
from datetime import datetime, timedelta


names = """
 Liam Smith
 Olivia Johnson
 Noah Williams
 Emma Brown
 Oliver Jones
 Ava Garcia
 Elijah Miller
 Charlotte Davis
 William Rodriguez
 Sophia Martinez
 James Hernandez
 Amelia Lopez
 Benjamin Gonzalez
 Isabella Wilson
 Lucas Anderson
 Mia Thomas
 Henry Taylor
 Evelyn Moore
 Alexander Jackson
 Harper Martin
 Michael Lee
 Camila Perez
 Ethan Thompson
 Gianna White
 Daniel Harris
 Abigail Sanchez
 Matthew Clark
 Luna Ramirez
 Jackson Lewis
 Ella Robinson
 Sebastian Walker
 Elizabeth Young
 Aiden Allen
 Sofia King
 Samuel Wright
 Avery Scott
 David Torres
 Mila Nguyen
 Joseph Hill
 Aria Flores
 Carter Green
 Scarlett Adams
 Owen Nelson
 Penelope Baker
 Wyatt Hall
 Chloe Rivera
 John Campbell
 Layla Mitchell
 Jack Carter
 Riley Roberts
 Luke Gomez
 Zoey Phillips
 Jayden Evans
 Nora Turner
 Dylan Diaz
 Lily Parker
 Grayson Cruz
 Eleanor Edwards
 Levi Collins
 Hannah Reyes
 Isaac Stewart
 Lillian Morris
 Gabriel Morales
 Addison Murphy
 Julian Cook
 Aubrey Rogers
 Mateo Gutierrez
 Ellie Ortiz
 Anthony Morgan
 Stella Cooper
 Jaxon Peterson
 Natalie Bailey
 Lincoln Reed
 Zoe Kelly
 Joshua Howard
 Leah Ramos
 Christopher Kim
 Hazel Cox
 Andrew Ward
 Violet Richardson
 Theodore Watson
 Aurora Brooks
 Caleb Chavez
 Savannah Wood
 Ryan James
 Brooklyn Bennett
 Asher Gray
 Bella Mendoza
 Nathan Ruiz
 Claire Hughes
 Thomas Price
 Skylar Alvarez
 Leo Castillo
 Lucy Sanders
 Isaiah Patel
 Paisley Myers
 Charles Long
 Everly Ross
 Josiah Foster
 Anna Jimenez
"""


DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Error loading Database url retrying")
    DATABASE_URL = os.getenv("DATABASE_URL")


names = [n.strip() for n in names.split('\n') if n.strip()]
first_names = [n.split()[0] for n in names]
last_names = [n.split()[-1] for n in names]


# cursor.execute("CREATE DATABASE IF NOT EXISTS testdb")
# cursor.execute("USE testdb")
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS test (
#    id INT AUTO_INCREMENT PRIMARY KEY,
#    first_name VARCHAR(50),
#    last_name VARCHAR(50),
#    email VARCHAR(100),
#    phone VARCHAR(20),
#    date_of_birth DATE,
#    gender VARCHAR(10),
#    address_line1 VARCHAR(255),
#    address_line2 VARCHAR(255),
#    city VARCHAR(100),
#    state VARCHAR(100),
#    postal_code VARCHAR(20),
#    country VARCHAR(100),
#    hire_date DATE,
#    job_title VARCHAR(100),
#    department VARCHAR(100),
#    salary DECIMAL(10,2),
#    manager_id INT,
#    status VARCHAR(20),
#    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# """)
#
#
# genders = ["Male", "Female", "Other"]
# cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
# states = ["NY", "CA", "IL", "TX", "AZ"]
# countries = ["USA", "Canada", "UK"]
# statuses = ["Active", "Inactive", "On Leave"]
# departments = ["HR", "IT", "Finance", "Sales", "Marketing"]
# job_titles = ["Manager", "Engineer", "Analyst", "Coordinator", "Specialist"]
#
#
# def maybe_null(value, probability=0.2):
#    """Return None with given probability, otherwise the value"""
#    return None if random.random() < probability else value
#
#
# for _ in range(1000):
#    first_name = maybe_null(random.choice(first_names))
#    last_name = maybe_null(random.choice(last_names))
#    email = maybe_null(f"{first_name.lower()}.{last_name.lower(
#    )}@example.com") if first_name and last_name else None
#    phone = maybe_null(f"+1{random.randint(1000000000, 9999999999)}")
#
#    dob = maybe_null(datetime.today() -
#                     timedelta(days=random.randint(7000, 20000)))
#    hire_date = maybe_null(
#        datetime.today() - timedelta(days=random.randint(0, 5000)))
#    gender = maybe_null(random.choice(genders))
#    address_line1 = maybe_null(f"{random.randint(100, 999)} Main St")
#    address_line2 = maybe_null("")
#    city = maybe_null(random.choice(cities))
#    state = maybe_null(random.choice(states))
#    postal_code = maybe_null(f"{random.randint(10000, 99999)}")
#    country = maybe_null(random.choice(countries))
#    job_title = maybe_null(random.choice(job_titles))
#    department = maybe_null(random.choice(departments))
#    salary = maybe_null(round(random.uniform(40000, 150000), 2))
#    manager_id = maybe_null(random.randint(1, 50))
#    status = maybe_null(random.choice(statuses))
#
#    cursor.execute("""
#        INSERT INTO test (
#            first_name, last_name, email, phone, date_of_birth, gender, address_line1,
#            address_line2, city, state, postal_code, country, hire_date, job_title,
#            department, salary, manager_id, status
#        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#    """, (
#        first_name, last_name, email, phone, dob.date(
#        ) if dob else None, gender, address_line1,
#        address_line2, city, state, postal_code, country, hire_date.date() if hire_date else None,
#        job_title, department, salary, manager_id, status
#    ))
#
# conn.commit()
# cursor.close()
# conn.close()
