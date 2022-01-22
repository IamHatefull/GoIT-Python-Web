import json
from random import randint
from datetime import date, timedelta


def create_grade_dict():
    grade_dict = {}
    index = 1

    for student_id in range(1,31):
        for _ in range(1, 21):
            grade = randint(50, 100)
            subject = randint(1,5)
            grade_date = (date(2021, 9, 1) + timedelta(days= (randint(1,120)))).strftime("%Y-%m-%d")
            grade_dict[index] = [grade, subject, student_id, grade_date]
            index += 1

    return grade_dict


def create_students_dict():
    student_id = [i for i in range(1,31)]
    group_id = [i for i in range(1,4)]
    students = ["James Walker", "Velma Clemons", "Kibo Underwood", "Louis Mcgee", "Phyllis Paul", "Zenaida Decker", 
                "Gillian Tillman", "Constance Boone", "Giselle Lancaster", "Kirsten Mcdowell", "Solomon Ray", "John Marshall",
                "Merrill Carney", "Hakeem Gillespie", "Hayden Boyer", "Griffin Mcleod", "Allistair Patton", "Rina Slater",
                "Caldwell Skinner", "Portia Galloway", "Noelle Valentine", "Abel Clay", "Stephanie Kent", "Axel Petty",
                "Nevada Morales", "Fuller Bush", "Quinn Mayo", "Marcia Shepard", "Kieran Moody", "Brielle Thompson"]
    student_dict = {}
    for id in student_id:
        if id < 11 :
            group_id = 1
        elif 11 <= id < 21:
            group_id = 2
        else:
            group_id = 3
        
        student_name = (students[id -1].split(' '))[0]
        student_surname = (students[id -1].split(' '))[1]
        student_dict[id] = [student_name, student_surname, group_id]

    return student_dict


def create_subject_dict():
    subject_dict = {1 : ["Biology", "John Smith"], 2 : ["Geography", "John Smith"], 3 : ["Economics", "Saliva Woords"], 4 : ["Math", "Saliva Woords"], 5 : ["English", "Fridrich Zumaba"]}
    return subject_dict


def create_groups_dict():
    groups_dict = {}
    for i in range(1, 4):
        groups_dict[i] = chr(randint(65, 90))  + chr(randint(65,90)) + str(randint(101, 200))
    return groups_dict
'''
groups_dict = create_groups_dict()
print(groups_dict)
with open('groups_dict.json','w') as fh:
    json.dump(groups_dict, fh)

students_dict = create_students_dict()
print(students_dict)
with open('students_dict.json','w') as fh:
    json.dump(students_dict, fh)

subjects_dict = create_subject_dict()
print(subjects_dict)
with open('subjects_dict.json','w') as fh:
    json.dump(subjects_dict, fh)'''

grades_dict = create_grade_dict()
print(grades_dict)
with open('grades_dict.json','w') as fh:
    json.dump(grades_dict, fh)
