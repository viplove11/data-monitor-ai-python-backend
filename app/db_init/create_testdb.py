import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import random
import datetime
from datetime import timedelta


first_names = ["Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava",
               "Elijah", "Charlotte", "William", "Sophia", "James", "Amelia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones",
              "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
cities = ["New York", "Los Angeles", "Chicago",
          "Houston", "Phoenix", "London", "Toronto", "Sydney"]
project_names = ["Apollo", "Zeus", "Athena",
                 "Hermes", "Ares", "Hera", "Poseidon", "Demeter"]
job_titles = ["Engineer", "Analyst", "Coordinator",
              "Specialist", "Architect", "Consultant"]


def maybe_null(value, probability=0.1):
    return None if random.random() < probability else value


def initDatabase():
    db_url = os.getenv(
        'DATABASE_URL', 'mysql+pymysql://root:31415@db:3306/testdb')
    try:
        engine = create_engine(db_url)

        with engine.connect() as connection:
            connection.execute("CREATE DATABASE IF NOT EXISTS testdb")
            connection.execute("USE testdb")

            connection.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    dept_id INT AUTO_INCREMENT PRIMARY KEY,
                    dept_name VARCHAR(100) UNIQUE NOT NULL,
                    budget DECIMAL(15,2),
                    location VARCHAR(100)
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    emp_id INT AUTO_INCREMENT PRIMARY KEY,
                    dept_id INT,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(100) UNIQUE,
                    hire_date DATE,
                    job_title VARCHAR(100),
                    salary DECIMAL(10,2),
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE SET NULL
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    project_id INT AUTO_INCREMENT PRIMARY KEY,
                    project_name VARCHAR(100) NOT NULL,
                    start_date DATE,
                    end_date DATE,
                    status VARCHAR(20)
                )
            """)

            connection.execute("""
                CREATE TABLE IF NOT EXISTS employee_projects (
                    emp_id INT,
                    project_id INT,
                    role VARCHAR(50),
                    hours_allocated INT,
                    PRIMARY KEY (emp_id, project_id),
                    FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE,
                    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
                )
            """)

            dept_data = [(f"Dept-{i}", round(random.uniform(500000, 5000000),
                          2), random.choice(cities)) for i in range(1, 11)]
            connection.executemany(
                "INSERT INTO departments (dept_name, budget, location) VALUES (%s, %s, %s)", dept_data)

            proj_data = []
            for name in project_names:
                start = datetime.today() - timedelta(days=random.randint(100, 1000))
                end = start + timedelta(days=random.randint(30, 365))
                proj_data.append((name, start.date(), end.date(),
                                 random.choice(["Active", "Completed", "On Hold"])))
            connection.executemany(
                "INSERT INTO projects (project_name, start_date, end_date, status) VALUES (%s, %s, %s, %s)", proj_data)

            emp_data = []
            for _ in range(1000):
                fname = random.choice(first_names)
                lname = random.choice(last_names)
                email = f"{fname.lower()}.{lname.lower()}_{ random.randint(1, 9999)}@corp.local"
                hire = datetime.today() - timedelta(days=random.randint(0, 3000))
                emp_data.append((
                    random.randint(1, 10),
                    fname, lname, email, hire.date(),
                    random.choice(job_titles),
                    round(random.uniform(50000, 150000), 2),
                    random.choice([True, False])
                ))
            connection.executemany("""
                INSERT INTO employees (dept_id, first_name, last_name, email, hire_date, job_title, salary, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, emp_data)

            mapping_data = set()
            while len(mapping_data) < 2000:
                emp_id = random.randint(1, 1000)
                proj_id = random.randint(1, len(project_names))
                role = random.choice(["Lead", "Contributor", "Reviewer"])
                hours = random.randint(10, 200)
                mapping_data.add((emp_id, proj_id, role, hours))

            connection.executemany(
                "INSERT INTO employee_projects (emp_id, project_id, role, hours_allocated) VALUES (%s, %s, %s, %s)", list(mapping_data))

            connection.commit()
        return None
    except OperationalError as err:
        return err
