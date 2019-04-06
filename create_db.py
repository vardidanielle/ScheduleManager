import atexit
import re
import sqlite3
import os
import sys

# Check if DB already exists BEFORE calling the connect, since connect will create it

_conn = sqlite3.connect('schedule.db')
DBExist = os.path.isfile('schedule.db')  # if the file exists


def create_table():
    _conn.executescript(""" 
        CREATE TABLE courses(
        id INTEGER PRIMARY KEY,
        course_name TEXT NOT NULL,
        student TEXT NOT NULL,
        number_of_students INTEGER NOT NULL,
        class_id INTEGER REFERENCES classrooms(id),
        course_length INTEGER NOT NULL
        );

        CREATE TABLE students(
        grade TEXT PRIMARY KEY,
        count INTEGER NOT NULL
        );

        CREATE TABLE classrooms(
        id INTEGER PRIMARY KEY,
        location TEXT NOT NULL,
        current_course_id INTEGER NOT NULL,
        current_course_time_left INTEGER NOT NULL
        );
        """)


def insert_course(id, course_name, student, number_of_students, class_id, course_length):
    _conn.execute("""
        INSERT INTO courses(id,course_name,student,number_of_students,class_id,course_length) VALUES (?,?,?,?,?,?)
        """, [id, course_name, student, number_of_students, class_id, course_length])


def insert_student(grade, count):
    _conn.execute("""
    INSERT INTO students (grade, count) VALUES (?,?)
    """, [grade, count])


def insert_classrooms(id, location, current_course_id, current_course_time_left):
    _conn.execute("""
        INSERT INTO classrooms (id, location,current_course_id, current_course_time_left) VALUES (?,?,?,?)
        """, [id, location, current_course_id, current_course_time_left])


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


def insert(lines):
    for line in lines:
        if len(line) != 0:
            line.strip()
            char = line[0]
            split_line = line.split(", ")
            if char == "S":
                grade = split_line[1].strip()
                count = split_line[2].strip()
                insert_student(grade, count)
            elif char == "C":
                id = split_line[1].strip()
                course_name = split_line[2].strip()
                student = split_line[3].strip()
                number_of_students = split_line[4].strip()
                class_id = split_line[5].strip()
                course_length = split_line[6].strip()
                insert_course(id, course_name, student, number_of_students, class_id, course_length)
            elif char == "R":
                id = split_line[1].strip()
                location = split_line[2].strip()
                location = location.split("\n")[0]
                insert_classrooms(id, location, 0, 0)


if __name__ == "__main__":
    create_table()
    file = open(sys.argv[1], 'r')
    lines = file.readlines()
    insert(lines)
    _conn.commit()
    c = _conn.cursor()
    print_table(("courses",))
    courses_array = c.execute("""
           SELECT * FROM courses""")
    all = c.fetchall()
    print_table(all)
    print_table(("classrooms",))
    rooms_array = c.execute("""
               SELECT * FROM classrooms""")
    all = c.fetchall()
    print_table(all)
    print_table(("students",))
    students_array = c.execute("""
           SELECT * FROM students""")
    all = c.fetchall()
    print_table(all)


def _close_db():
    _conn.commit()
    _conn.close()


atexit.register(_close_db)

