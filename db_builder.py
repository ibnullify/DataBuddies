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
def make_id_to_name_dict():
    command = "SELECT name, id FROM peeps;" #Get names and Ids of all students
    result = c.execute(command)
    dict = {}
    for student in result:
        #print student
        #Dict of ID to student
        dict[student[1]] = student[0]
    return dict

'''
Takes in a student name and a names_to_grade dict
Returns the grades of the student
'''
def get_grades(student, names_to_grades):
    return names_to_grades[student]

'''
Takes in a student and a names_to_grade dict
Returns the average of that student
'''
def calculate_avg(student, names_to_grades):
    sum = 0
    count = 0
    grade_dict = get_grades(student, names_to_grades)
    for grade in grade_dict.values():
        sum += grade
        count += 1
    return float(sum/count)

'''
Creates a Dictionary with every student as an entry
Each student is mapped to an int which is their id
'''
def make_students_to_ids_dict():
   command = "SELECT name, peeps.id FROM peeps;"
   result = c.execute(command)
   dict = {}
   #Results returns a touple of:
   #(name, ID)
   for name_id in result:
       #print name_id
       #{Student name : ID, Student name: {...}, ...}
       name = name_id[0].encode('utf-8')[:-1] #Remove the unicode character and the trialing space
       if not name in dict: #If this is the first  we see of the student
           dict[name] = name_id[1] #Create a new dict for them and place their first grade
   #print(dict)
   return dict
    
'''
prints the combination of the name, id, and average of a student
'''    
def display_name_id_avg(student,students_to_ids,names_to_grades):
    avg = calculate_avg(student, names_to_grades)
    #print students_to_ids["TOKiMONSTA"]
    id = students_to_ids[student]
    #print student + ", " + id + ", " + avg
    print student,id,avg
    

def main():
    populate()
    names_to_grades = make_name_to_grade_dict()
    ids_to_names = make_id_to_name_dict()
    students_to_ids = make_students_to_ids_dict()
    #print calculate_avg("TOKiMONSTA", names_to_grades)
    #print calculate_avg("sasha", names_to_grades)
    display_name_id_avg("TOKiMONSTA",students_to_ids,names_to_grades)
    display_name_id_avg("sasha",students_to_ids,names_to_grades)
    db.commit() #save changes
    db.close()  #close database


main()
