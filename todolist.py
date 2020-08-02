from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

# Create Database file
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

# Create Table
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='task_description')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


# Create Database
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def todays_task(date=None):
    if date is None:
        today = datetime.today()
        print(f'\nToday {today.day} {today.strftime("%b")}:')
    else:
        today = date
        print(f'\n{today.strftime("%A")} {today.day} {today.strftime("%b")}:')
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print_tasks(rows)


def print_tasks(rows, style="day"):
    text_format1 = '{0}. {1}'
    text_format2 = '{0}. {1}. {2}'
    if len(rows) >= 1 and style == "day":
        for num, row in enumerate(rows, start=1):
            print(text_format1.format(num, row))
    elif len(rows) > 1 and style == "all":
        for num, row in enumerate(rows, start=1):
            date = row.deadline
            date = f'{date.day} {date.strftime("%b")}'
            print(text_format2.format(num, row, date))
    else:
        print("Nothing to do!")


def weeks_task():
    today = datetime.today()
    for day in range(7):
        date = today + timedelta(days=day)
        todays_task(date)


def all_tasks():
    print("\nAll tasks:")
    rows = session.query(Table).order_by(Table.deadline).all()
    print_tasks(rows, style="all")


def add_task():
    print("\nEnter task")
    task_inp = input()
    print("Enter deadline")
    task_date = input()
    if task_date is None:
        task_date = datetime.today()
    else:
        task_date = datetime.strptime(task_date, "%Y-%m-%d")
    new_row = Table(task=task_inp, deadline=task_date)
    session.add(new_row)
    session.commit()
    print("The task has been added!")


def missed_tasks():
    print("\nMissed tasks:")
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline < today.date()).order_by(Table.deadline).all()
    if len(rows) >= 1:
        print_tasks(rows, style="all")
    else:
        print("Nothing is missed!")


def delete_task():
    print("\nChoose the number of the task you want to delete:")
    rows = session.query(Table).order_by(Table.deadline).all()
    print_tasks(rows, style="all")
    try:
        inp = int(input())
    except ValueError:
        print("Invalid Input")
        return
    session.delete(rows[inp-1])
    session.commit()
    print("The task has been deleted!")


def menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    try:
        inp = int(input())
    except ValueError:
        print("Invalid Input")
        return
    if inp == 1:
        todays_task()
    elif inp == 2:
        weeks_task()
    elif inp == 3:
        all_tasks()
    elif inp == 4:
        missed_tasks()
    elif inp == 5:
        add_task()
    elif inp == 6:
        delete_task()
    elif inp == 0:
        print("\nBye")
        quit()
    else:
        print("Invalid Input")


while True:
    menu()
    print()
