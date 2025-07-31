import random
from faker import Faker
from sqlalchemy import (
    create_engine, MetaData, Table, Column,
    Integer, String, Float, ForeignKey, Date
)
from datetime import datetime, timedelta

DB_URL = "postgresql://myuser:mypassword@localhost:5432/postgres"

naming_convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

fake = Faker()
engine = create_engine(DB_URL)
metadata = MetaData(naming_convention=naming_convention)

departments = Table('departments', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('building', String),
    Column('budget', Float),
    Column('established', Date),
    Column('chair_id', Integer, ForeignKey('professors.id'))
)

professors = Table('professors', metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('email', String, unique=True),
    Column('salary', Float),
    Column('dept_id', Integer, ForeignKey('departments.id'))
)

students = Table('students', metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('email', String, unique=True),
    Column('enroll_date', Date),
    Column('advisor_id', Integer, ForeignKey('professors.id'))
)

courses = Table('courses', metadata,
    Column('id', Integer, primary_key=True),
    Column('code', String, unique=True),
    Column('title', String),
    Column('credits', Integer),
    Column('dept_id', Integer, ForeignKey('departments.id')),
    Column('level', String)
)

classes = Table('classes', metadata,
    Column('id', Integer, primary_key=True),
    Column('course_id', Integer, ForeignKey('courses.id')),
    Column('professor_id', Integer, ForeignKey('professors.id')),
    Column('room', String),
    Column('capacity', Integer),
    Column('schedule', String)
)

enrollments = Table('enrollments', metadata,
    Column('id', Integer, primary_key=True),
    Column('class_id', Integer, ForeignKey('classes.id')),
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('grade', String),
    Column('enroll_date', Date),
    Column('status', String)
)

advisors = Table('advisors', metadata,
    Column('id', Integer, primary_key=True),
    Column('professor_id', Integer, ForeignKey('professors.id')),
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('assigned_date', Date),
    Column('role', String),
    Column('notes', String)
)

rooms = Table('rooms', metadata,
    Column('id', Integer, primary_key=True),
    Column('room_number', String),
    Column('building', String),
    Column('capacity', Integer),
    Column('type', String),
    Column('equipment', String)
)

schedules = Table('schedules', metadata,
    Column('id', Integer, primary_key=True),
    Column('class_id', Integer, ForeignKey('classes.id')),
    Column('day_of_week', String),
    Column('start_time', String),
    Column('end_time', String),
    Column('location', String)
)

metadata.create_all(engine, checkfirst=True)

conn = engine.connect()

dept_ids = []
for _ in range(10):
    res = conn.execute(departments.insert().values(
        name=fake.company(),
        building=fake.street_name(),
        budget=round(random.uniform(1e5, 1e6), 2),
        established=fake.date_between(start_date='-50y', end_date='today'),
        chair_id=None
    ))
    dept_ids.append(res.inserted_primary_key[0])

prof_ids = []
for _ in range(200):
    dept = random.choice(dept_ids)
    res = conn.execute(professors.insert().values(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        salary=round(random.uniform(50000, 150000), 2),
        dept_id=dept
    ))
    prof_ids.append(res.inserted_primary_key[0])

for did in dept_ids:
    chair = random.choice(prof_ids)
    conn.execute(departments.update().where(departments.c.id==did)
                 .values(chair_id=chair))

stud_ids = []
for _ in range(500):
    advisor = random.choice(prof_ids)
    res = conn.execute(students.insert().values(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
        enroll_date=fake.date_between(start_date='-4y', end_date='today'),
        advisor_id=advisor
    ))
    stud_ids.append(res.inserted_primary_key[0])

course_ids = []
for i in range(50):
    dept = random.choice(dept_ids)
    res = conn.execute(courses.insert().values(
        code=f"C{i+100}",
        title=fake.bs().title(),
        credits=random.randint(1,4),
        dept_id=dept,
        level=random.choice(['Undergrad','Grad'])
    ))
    course_ids.append(res.inserted_primary_key[0])

class_ids = []
for _ in range(200):
    res = conn.execute(classes.insert().values(
        course_id=random.choice(course_ids),
        professor_id=random.choice(prof_ids),
        room=str(random.randint(100,499)),
        capacity=random.randint(20,100),
        schedule=random.choice(['MWF 9-10','TTh 11-12','MWF 2-3'])
    ))
    class_ids.append(res.inserted_primary_key[0])

for _ in range(1000):
    conn.execute(enrollments.insert().values(
        class_id=random.choice(class_ids),
        student_id=random.choice(stud_ids),
        grade=random.choice(['A','B','C','D','F']),
        enroll_date=fake.date_between(start_date='-1y', end_date='today'),
        status=random.choice(['enrolled','dropped','completed'])
    ))

for _ in range(500):
    conn.execute(advisors.insert().values(
        professor_id=random.choice(prof_ids),
        student_id=random.choice(stud_ids),
        assigned_date=fake.date_between(start_date='-4y', end_date='today'),
        role=random.choice(['academic','thesis']),
        notes=fake.sentence()
    ))

for _ in range(20):
    conn.execute(rooms.insert().values(
        room_number=str(random.randint(100,599)),
        building=fake.street_name(),
        capacity=random.randint(20,200),
        type=random.choice(['Lecture','Lab','Seminar']),
        equipment=", ".join(fake.words(3))
    ))

days = ['Monday','Tuesday','Wednesday','Thursday','Friday']
for _ in range(500):
    conn.execute(schedules.insert().values(
        class_id=random.choice(class_ids),
        day_of_week=random.choice(days),
        start_time=f"{random.randint(8,16)}:00",
        end_time=f"{random.randint(9,18)}:00",
        location=f"Building {fake.building_number()}"
    ))

conn.close()
print("✅ Seeded database with 10 tables and related data.")
