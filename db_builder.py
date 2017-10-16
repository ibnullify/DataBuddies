'''
Anish Shenoy
SoftDev1 pd7
HW<09 -- No Treble
2017-10-14
'''

import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
#import os Used for os.remove()

f="discobandit.db"
#os.remove(f) Used During Testing to remove file at the beginning

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

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

populate()

#==========================================================
db.commit() #save changes
db.close()  #close database
