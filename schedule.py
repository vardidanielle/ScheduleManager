import os
import sqlite3

DBExist = os.path.isfile('schedule.db')  # if the file exists
loop = True


def print_table(list_of_tuples):
    for item in list_of_tuples:
        print(item)


if DBExist:
    _conn = sqlite3.connect('schedule.db')
    c = _conn.cursor()
    courses = c.execute("SELECT * FROM courses").fetchall()
    counter = 0
    while len(courses) != 0:
        loop = False
        classrooms = c.execute("SELECT * FROM classrooms").fetchall()
        for classroom in classrooms:
            class_id = classroom[0]
            if classroom[3] == 1 or classroom[3] == 0:  # current_course_time_left = 0 or ==1 because now it will be
                # done (either empty or done)
                if classroom[2] != 0:  # there is a class in there
                    course_id = classroom[2]
                    current_course = c.execute(
                        "SELECT course_name FROM courses WHERE id= {}".format(course_id)).fetchone()
                    print("(" + str(counter) + ") " + classroom[1] + ": " + current_course[0] + " is done")
                    c.execute("""DELETE FROM courses WHERE id = {}""".format(course_id))  # delete the course that
                    # finished studying
                    _conn.commit()
                courses = c.execute("""SELECT * FROM courses WHERE class_id = {}""".format(class_id))
                course = courses.fetchone()
                if course:
                    x = c.execute("""SELECT students.grade, courses.number_of_students, students.count FROM courses 
                                INNER JOIN students ON courses.student = students.grade and courses.id = {}""".format
                                  (course[0])).fetchone()
                    c.execute("""UPDATE students SET count = {} WHERE grade = '{}'""".format(x[2] - x[1], x[0]))
                    _conn.commit()
                    c.execute("""UPDATE classrooms
                                SET current_course_id = {}, current_course_time_left = {}
                                WHERE id = {}""".format(course[0], course[5], class_id))
                    _conn.commit()
                    print("(" + str(counter) + ") " + classroom[1] + ": " + course[1] + " is schedule to start")
                else:
                    c.execute("""UPDATE classrooms SET current_course_id = {}, current_course_time_left = {}
                                WHERE id = {}""".format(0, 0, class_id))  # update the current class id and time left
                    # to 0
                    _conn.commit()
            else:
                course_name = c.execute("""SELECT course_name FROM courses WHERE id = '{}'""".format(classroom[2]))\
                    .fetchone()
                print("(" + str(counter) + ") " + classroom[1] + ": occupied by " + str(course_name[0]))
                one_hour_less = classroom[3] - 1
                c.execute("""UPDATE classrooms
                            SET current_course_time_left = {}
                            WHERE id = {}""".format(one_hour_less, class_id))
                _conn.commit()
        print_table(("courses",))
        courses_array = c.execute("SELECT * FROM courses")
        all = c.fetchall()
        print_table(all)
        print_table(("classrooms",))
        rooms_array = c.execute("SELECT * FROM classrooms")
        all = c.fetchall()
        print_table(all)
        print_table(("students",))
        students_array = c.execute("SELECT * FROM students")
        all = c.fetchall()
        print_table(all)
        courses = c.execute("SELECT * FROM courses").fetchall()
        counter = counter+1
    if loop:
        print_table(("courses",))
        courses_array = c.execute("SELECT * FROM courses")
        all = c.fetchall()
        print_table(all)
        print_table(("classrooms",))
        rooms_array = c.execute("SELECT * FROM classrooms")
        all = c.fetchall()
        print_table(all)
        print_table(("students",))
        students_array = c.execute("SELECT * FROM students")
        all = c.fetchall()
        print_table(all)
        courses = c.execute("SELECT * FROM courses").fetchall()
        counter = counter + 1
else:
    print("schedule.db not found")