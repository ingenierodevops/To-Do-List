# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_task')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def print_today_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print("Today", str(today.day), today.strftime('%b') + ":")
    if rows:
        for row in rows:
            print(str(row.id) + ". ", end="")  # Will print the id of the row.
            print(row.task)  # Will print value of the task field
            # print(row.deadline.day, row.deadline.strftime('%b'))  # Will print value of the deadline field
            # print(row)  # Will print the string that was returned by __repr__ method
    else:
        print("Nothing to do!")
        print()


def print_week_tasks():
    num_dia = 0
    today = datetime.today()
    while num_dia < 7:
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        print(today.strftime('%A'), str(today.day), today.strftime('%b') + ":")
        if rows:
            for row in rows:
                print(str(row.id) + '. ', end="")  # Will print the id of the row.
                print(row.task)  # Will print value of the task field
                # print(row.deadline.day, row.deadline.strftime('%b'))  # Will print value of the deadline field
                # print(row)  # Will print the string that was returned by __repr__ method
        else:
            print("Nothing to do!")
        print()
        num_dia += 1
        today = today + timedelta(days=1)


def print_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    if rows:
        number = 1
        for row in rows:
            print(str(number) + '. ', end="")  # Will print the id of the row.
            print(row.task + '. ', end="")  # Will print value of the task field
            print(row.deadline.day, row.deadline.strftime('%b'))  # Will print value of the deadline field
            number = number + 1
            #print(row)  # Will print the string that was returned by __repr__ method
    else:
        print("Nothing to do!")
        print()


def add_tasks(texto, dead):
    fecha_dead = datetime.strptime(dead, '%Y-%m-%d')
    new_row = Table(task=texto,
                    deadline=fecha_dead)
    session.add(new_row)
    session.commit()
    print("The task has been added!")

def menu():
    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Add task
0) Exit""")

while True:
    menu()
    option = int(input())
    if option == 1:
        print_today_tasks()
    elif option == 2:
        print_week_tasks()
    elif option == 3:
        print_tasks()
    elif option == 4:
        print("Enter task")
        task_text = input()
        print("Enter deadline")
        task_deadline = input()
        add_tasks(task_text, task_deadline)
    elif option == 0:
        print("Bye!")
        break
