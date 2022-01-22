import sqlite3, json
from sqlite3 import Error
from contextlib import contextmanager
from pathlib import Path
from datetime import date, datetime

@contextmanager
def create_connection(db_file):
    ''' create a database connection to a Students database'''
    try:
        conn = sqlite3.connect(db_file)
        yield(conn)
        conn.commit()
    except Error as e:
        conn.rollback()
        print(e)
    finally:
        conn.close()


def create_table(conn, create_table_statement):
    ''' create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    '''
    try:
        c = conn.cursor()
        c.execute(create_table_statement)
    except Error as e:
        print(e)


def add_data(conn,data_statement):
    '''Add data to table using connection and SQL query'''

    try:
        cur = conn.cursor()
        cur.execute(data_statement)
    finally:
        cur.close()


def get_data(conn, data_query):
    '''Get data from database using connection and SQL query and then returns it'''
    try:
        cur = conn.cursor()
        cur.execute(data_query)
        res = cur.fetchall()
        return res
    finally:
        cur.close()

#Database path
students_db = "./students_db"

#Query to create students table
create_students_table = ''' CREATE TABLE IF NOT EXISTS students(
    student_id INT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    surname VARCHAR(30) NOT NULL,
    group_id INT,
    FOREIGN KEY (group_id) REFERENCES groups (group_id)
        ON DELETE CASCADE
    );'''

#Query to create groups table
create_groups_table = ''' CREATE TABLE IF NOT EXISTS groups(
    group_id INT PRIMARY KEY,
    group_name VARCHAR(30) NOT NULL
    );'''

#Query to create subjects table
create_subjects_table = ''' CREATE TABLE IF NOT EXISTS subjects(
    subject_id INT PRIMARY KEY,
    subject_name VARCHAR(30) NOT NULL,
    lecturer_name VARCHAR(30) NOT NULL
    );'''

#Query to create grades table
create_grades_table = ''' CREATE TABLE IF NOT EXISTS grades(
    grade_id INT PRIMARY KEY,
    grade_name INT NOT NULL,
    subject_id INT,
    student_id INT,
    grade_data DATE NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE
    );'''

#Querys to insert data into each table
insert_students_value = """ INSERT INTO students(student_id, name, surname, group_id) VALUES({},'{}','{}',{})"""
insert_groups_value = """ INSERT INTO groups (group_id, group_name) VALUES({}, '{}')"""
insert_subjects_value = """ INSERT INTO subjects(subject_id, subject_name, lecturer_name) VALUES({},'{}','{}')"""
insert_grades_value = """ INSERT INTO grades(grade_id, grade_name, subject_id, student_id, grade_data) VALUES({},{},{},{},'{}')"""


def create_all_data():
    '''Create database, create all tables and add all data into it. 
    Data was taken from json files which was created by "db_data.py".'''

    with create_connection(students_db) as conn:
        if conn is not None:

            create_table(conn, create_students_table)

            create_table(conn, create_groups_table)

            create_table(conn, create_subjects_table)

            create_table(conn, create_grades_table)

            print('Tables were succesfully created!!')



        else:
            print("Database connection was NOT created!")

    #Saving data from json files into variables
    with open("grades_dict.json", "r") as fh:
        grades_dict = json.load(fh)

    with open("groups_dict.json", "r") as fh:
        groups_dict = json.load(fh)

    with open("students_dict.json", "r") as fh:
        students_dict = json.load(fh)

    with open("subjects_dict.json", "r") as fh:
        subjects_dict = json.load(fh)

    #Inserting data into each table
    with create_connection(students_db) as conn:
        if conn is not None:

            #"i" is "id" in each table
            i = 1
            for value in groups_dict.values():
                add_data(conn, insert_groups_value.format(i,value))
                i +=1

            i = 1
            for value in students_dict.values():
                add_data(conn, (insert_students_value.format(i, value[0], value[1],value[2])))
                i += 1

            i = 1
            for value in subjects_dict.values():
                add_data(conn, insert_subjects_value.format(i, value[0], value[1]))
                i += 1

            i = 1
            for value in grades_dict.values():
                add_data(conn, insert_grades_value.format(i, value[0], value[1], value[2], datetime.date(datetime.strptime(value[3], '%Y-%m-%d'))))
                i += 1


def get_all_data():
    '''Geting all data needed by tasks and printing it'''


    #1) 5 students with the highest average score in all subjects.
    #2) 1 student with the highest GPA in one subject.
    #3) the average score in the group in one subject.
    #4) Average score in the stream.
    #5) What courses does the teacher read.
    #6) List of students in the group.
    #7) Grades of students in the group on the subject.
    #8) Grades of students in the group on the subject at the last lesson.
    #9) List of courses the student is attending.
    #10) A list of courses that the teacher reads to the student.
    #11) The average score that the teacher puts to the student.
    #12) The average score given by the teacher.

    task_1 = '''SELECT students.student_id,  students.name, students.surname, AVG(grades.grade_name) AS grade FROM students JOIN grades
                ON students.student_id = grades.student_id
                GROUP BY students.student_id 
                ORDER BY grade DESC
                LIMIT 5'''

    task_2 = ''' SELECT student_id,  AVG(grade_name) AS grade, subject_id FROM grades
                GROUP BY student_id, subject_id
                ORDER BY subject_id, grade DESC 
                LIMIT 1;'''

    task_3 = ''' SELECT groups.group_name, AVG(grades.grade_name), grades.subject_id
                FROM  groups JOIN students ON groups.group_id = students.group_id
                JOIN grades ON students.student_id = grades.student_id
                WHERE students.group_id = 1 AND grades.subject_id = 1
                GROUP BY groups.group_name, grades.subject_id; '''

    task_4 = ''' SELECT AVG(grade_name) FROM grades;'''

    task_5 = ''' SELECT lecturer_name, subject_name FROM subjects ORDER BY lecturer_name;'''

    task_6 = ''' SELECT name, surname FROM students WHERE group_id = 1;'''

    task_7 = ''' SELECT grades.grade_name, students.name, students.surname, students.group_id 
                FROM grades JOIN students 
                ON grades.student_id = students.student_id 
                WHERE grades.subject_id = 1 AND students.group_id = 1;'''

    task_8 = ''' SELECT grades.grade_name, grades.grade_data, students.name, students.group_id, grades.subject_id 
                FROM grades JOIN students 
                ON grades.student_id = students.student_id
                WHERE grades.grade_data = '2021-12-30' AND students.group_id = 1 AND grades.subject_id = 3
                ORDER BY grades.grade_data DESC;'''

    task_9 = ''' SELECT students.student_id, students.name, students.surname, subjects.subject_name
                FROM students JOIN grades ON students.student_id = grades.student_id
                JOIN subjects ON grades.subject_id = subjects.subject_id; '''

    task_10 = ''' SELECT DISTINCT students.student_id, students.name, students.surname, subjects.subject_name, subjects.lecturer_name
                FROM students JOIN grades ON students.student_id = grades.student_id
                JOIN subjects ON grades.subject_id = subjects.subject_id
                ORDER BY subjects.lecturer_name; '''

    task_11 = ''' SELECT students.name, AVG(grades.grade_name), subjects.lecturer_name FROM students JOIN grades 
                ON students.student_id = grades.student_id 
                JOIN subjects 
                ON grades.subject_id = subjects.subject_id 
                GROUP BY students.name, subjects.lecturer_name
                ORDER BY subjects.lecturer_name;'''

    task_12 = ''' SELECT subjects.lecturer_name, AVG(grades.grade_name) 
                FROM grades JOIN subjects ON grades.subject_id = subjects.subject_id 
                GROUP BY subjects.lecturer_name;'''

    with create_connection(students_db) as conn:
        if conn is not None:

            data_1 = get_data(conn, task_1)
            print(data_1)

            data_2 = get_data(conn, task_2)
            print(data_2)

            data_3 = get_data(conn, task_3)
            print(data_3)

            data_4 = get_data(conn, task_4)
            print(data_4)

            data_5 = get_data(conn, task_5)
            print(data_5)

            data_6 = get_data(conn, task_6)
            print(data_6)

            data_7 = get_data(conn, task_7)
            print(data_7)

            data_8 = get_data(conn, task_8)
            print(data_8)

            data_9 = get_data(conn, task_9)
            print(data_9)

            data_10 = get_data(conn, task_10)
            print(data_10)

            data_11 = get_data(conn, task_11)
            print(data_11)

            data_12 = get_data(conn, task_12)
            print(data_12)

        else:
            print("Database connection was NOT created!")


if __name__ == "__main__":
    create_all_data()
    get_all_data()
    