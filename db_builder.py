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

def main():
    populate()
    students_to_grades = makeDict()

    db.commit() #save changes
    db.close()  #close database

'''
Creates a Dictionary with every student as an entry
Each student is mapped to another Dictionary
Which contains all of the classes theyve take and recieved a grade for
'''
def makeDict():
    command = "SELECT name, peeps.id, mark, code FROM peeps, courses WHERE peeps.id = courses.id;"
    result = c.execute(command)
    dict = {}
    #Results returns a touple of:
    #(name, ID, Grade, class)
    for grade in result:
        #{Student name : {Class: Grade, Class: Grade, ...}, Student name: {...}, ...}
        if not grade[0] in dict: #If this is the first grade we see of the student
            dict[grade[0]] = {grade[3]:grade[2]} #Create a new dict for them and place their first grade
        else:
            dict[grade[0]][grade[3]] = grade[2] #Otherwise add their new grade
    #print(dict)
    return dict

main()
