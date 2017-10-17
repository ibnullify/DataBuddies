'''
Anish Shenoy
SoftDev1 pd7
HW<09 -- No Treble
2017-10-14
'''

import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import os #Used for os.remove()

f="discobandit.db"
os.remove(f) #Used During Testing to remove file at the beginning

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

def populate():
    input_file = csv.DictReader(open("peeps.csv"))#Reads CSV
    c.execute("CREATE TABLE peeps(name TEXT, age INTEGER, id INTEGER)")
    for row in input_file:
        #print row
        command = "INSERT INTO peeps VALUES (\"" + row["name"] + " \", " + row["age"] +  ", " + row["id"] + ")"
        c.execute(command)

    input_file = csv.DictReader(open("courses.csv"))#Reads CSV
    c.execute("CREATE TABLE courses(code TEXT, mark INTEGER, id INTEGER)")
    for row in input_file:
        #print row
        command = "INSERT INTO courses VALUES (\"" + row["code"] + " \", " + row["mark"] +  ", " + row["id"] + ")"
        c.execute(command)

'''
Creates a Dictionary with every student as an entry
Each student is mapped to another Dictionary
Which contains all of the classes theyve take and recieved a grade for
'''
def make_name_to_grade_dict():
    command = "SELECT name, peeps.id, mark, code FROM peeps, courses WHERE peeps.id = courses.id;"
    result = c.execute(command)
    dict = {}
    #Results returns a touple of:
    #(name, ID, Grade, class)
    for grade in result:
        #{Student name : {Class: Grade, Class: Grade, ...}, Student name: {...}, ...}
        name = grade[0].encode('utf-8')[:-1] #Remove the unicode character and the trialing space
        if not name in dict: #If this is the first grade we see of the student
            dict[name] = {grade[3]:grade[2]} #Create a new dict for them and place their first grade
        else:
            dict[name][grade[3]] = grade[2] #Otherwise add their new grade
    #print(dict)
    return dict

'''
Creates a Dictionary with every ID mapped to the student name
'''
def Id_to_name():
    command = "SELECT name, id FROM peeps;" #Get names and Ids of all students
    result = c.execute(command)
    dict = {}
    for student in result:
        #Dict of ID to student
        dict[student[1]] = student[0]
    return dict

'''
Takes in a student name and a names_to_grade dict
Returns the grades of the student
'''
def getGrades(student, names_to_grades):
    return names_to_grades[student]

'''
Takes in a student and a names_to_grade dict
Returns the average of that student
'''
def calculate_avg(student, names_to_grades):
    sum = 0
    count = 0
    grade_dict = getGrades(student, names_to_grades)
    for grade in grade_dict.values():
        sum += grade
        count += 1
    return float(sum/count)

#def display_name_id_avg():


def main():
    populate()
    names_to_grades = make_name_to_grade_dict()
    ids_to_names = Id_to_name()
    #print calculate_avg("TOKiMONSTA", names_to_grades)
    print calculate_avg("sasha", names_to_grades)
    db.commit() #save changes
    db.close()  #close database


main()
