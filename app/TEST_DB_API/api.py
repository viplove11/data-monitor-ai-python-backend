import random
from datetime import datetime, timedelta
from sqlalchemy import text
first_names = ["Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava", "Elijah",
               "Charlotte", "William", "Sophia", "James", "Amelia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
              "Miller", "Davis", "Rodriguez", "Martinez"]
cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "London",
          "Toronto", "Sydney"]
project_names = ["Apollo", "Zeus", "Athena",
                 "Hermes", "Ares", "Hera", "Poseidon", "Demeter"]
job_titles = ["Engineer", "Analyst", "Coordinator", "Specialist", "Architect",
              "Consultant"]


def initDatabase(engine):
    try:
        with engine.begin() as connection:
            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS  departments(
                    dept_id INT AUTO_INCREMENT PRIMARY KEY,
                    dept_name VARCHAR(100) UNIQUE NOT NULL,
                    budget DECIMAL(15,2),
                    location VARCHAR(100)
                )
            """))

            connection.execute(text("""
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
            """))

            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS projects (
                    project_id INT AUTO_INCREMENT PRIMARY KEY,
                    project_name VARCHAR(100) NOT NULL,
                    start_date DATE,
                    end_date DATE,
                    status VARCHAR(20)
                )
            """))

            connection.execute(text("""
                CREATE TABLE IF NOT EXISTS employee_projects (
                    emp_id INT,
                    project_id INT,
                    role VARCHAR(50),
                    hours_allocated INT,
                    PRIMARY KEY (emp_id, project_id),
                    FOREIGN KEY (emp_id) REFERENCES employees(emp_id) ON DELETE CASCADE,
                    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
                )
            """))

            dept_data = [
                {"dept_name": f"Dept-{i}", "budget": round(random.uniform(
                    500000, 5000000), 2), "location": random.choice(cities)}
                for i in range(1, 11)
            ]

            connection.execute(text(
                "INSERT IGNORE INTO departments (dept_name, budget, location) VALUES (:dept_name, :budget, :location)"), dept_data)

            proj_data = []
            for name in project_names:
                start = datetime.today() - timedelta(days=random.randint(100, 1000))
                end = start + timedelta(days=random.randint(30, 365))
                proj_data.append({
                    "project_name": name,
                    "start_date": start.date(),
                    "end_date": end.date(),
                    "status": random.choice(["Active", "Completed", "On Hold"])
                })
            connection.execute(text(
                "INSERT IGNORE INTO projects (project_name, start_date, end_date, status) VALUES (:project_name, :start_date, :end_date, :status)"), proj_data)

            emp_data = []
            for _ in range(1000):
                fname = random.choice(first_names)
                lname = random.choice(last_names)
                email = f"{fname.lower()}.{lname.lower()}_{ random.randint(1, 99999)}@corp.local"
                hire = datetime.today() - timedelta(days=random.randint(0, 3000))
                emp_data.append({
                    "dept_id": random.randint(1, 10),
                    "first_name": fname,
                    "last_name": lname,
                    "email": email,
                    "hire_date": hire.date(),
                    "job_title": random.choice(job_titles),
                    "salary": round(random.uniform(50000, 150000), 2),
                    "is_active": random.choice([True, False])
                })
            connection.execute(text("""
                INSERT IGNORE INTO employees (dept_id, first_name, last_name, email, hire_date, job_title, salary, is_active)
                VALUES (:dept_id, :first_name, :last_name, :email, :hire_date, :job_title, :salary, :is_active)
            """), emp_data)

            mapping_data = set()
            while len(mapping_data) < 2000:
                mapping_data.add((
                    random.randint(1, 1000),
                    random.randint(1, len(project_names)),
                    random.choice(["Lead", "Contributor", "Reviewer"]),
                    random.randint(10, 200)
                ))

            mapping_dicts = [{"emp_id": m[0], "project_id": m[1],
                              "role": m[2], "hours": m[3]} for m in mapping_data]
            connection.execute(text(
                "INSERT IGNORE INTO employee_projects (emp_id, project_id, role, hours_allocated) VALUES (:emp_id, :project_id, :role, :hours)"), mapping_dicts)

        return None
    except Exception as err:
        return err


def flatten(lst):
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def print_db(engine):
    try:
        with engine.begin() as connection:
            output = {}
            tables = [row[0] for row in connection.execute(text("SHOW TABLES"))]
            for table in tables:
                output[table] = [x for row in connection.execute(text(f"SELECT * FROM {table}")) for x in row]
            return output, None
    except Exception as err:
        return "", err
