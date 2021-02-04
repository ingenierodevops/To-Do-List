# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
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


def print_tasks():
    rows = session.query(Table).all()
    if rows:
        for row in rows:
            print(row.id)  # Will print the id of the row.
            print(row.task)  # Will print value of the task field
            print(row.deadline)  # Will print value of the deadline field
            print(row)  # Will print the string that was returned by __repr__ method
    else:
        print("Nothing to do!")

def add_tasks(texto):
    new_row = Table(task=texto,
                    deadline=datetime.today())
    session.add(new_row)
    session.commit()
    print("The task has been added!")

def menu():
    print("""1) Today's tasks
2) Add task
0) Exit""")

while True:
    menu()
    option = int(input())
    if option == 1:
        print_tasks()
    elif option == 2:
        print("Enter task")
        task_text = input()
        add_tasks(task_text)
    elif option == 0:
        print("Bye!")
        break
