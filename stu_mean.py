'''
Anish Shenoy, Ibnul Jahan
SoftDev1 pd7
HW10 -- Average
2017-10-17
'''

import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O
import os #Used for os.remove()

f="discobandit.db"
os.remove(f) #Used During Testing to remove file at the beginning

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

names_to_grades = {}
ids_to_names = {}
students_to_ids = {}

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
def make_names_to_grades_dict():
    command = "SELECT name, peeps.id, mark, code FROM peeps, courses WHERE peeps.id = courses.id;"
    result = c.execute(command)
    dict = {}
    #Results returns a touple of:
    #(name, ID, Grade, class)
    for grade in result:
        #{Student name : {Class: Grade, Class: Grade, ...}, Student name: {...}, ...}
        name = grade[0].encode('utf-8')[:-1] #Remove the unicode character and the trialing space
        course = grade[3].encode('utf-8')[:-1]
        if not name in dict: #If this is the first grade we see of the student
            dict[name] = {course:grade[2]} #Create a new dict for them and place their first grade
        else:
            dict[name][course] = grade[2] #Otherwise add their new grade
    #print(dict)
    return dict

'''
Creates a Dictionary with every ID mapped to the student name
'''
def make_ids_to_names_dict():
    command = "SELECT name, id FROM peeps;" #Get names and Ids of all students
    result = c.execute(command)
    dict = {}
    for student in result:
        #print student
        #Dict of ID to student
        dict[student[1]] = student[0].encode('utf-8')[:-1]
    return dict

'''
Takes in a student name and a names_to_grade dict
Returns the grades of the student
'''
def get_grades(student):
    return names_to_grades[student]

'''
Takes in a student and a names_to_grade dict
Returns the average of that student
'''
def calculate_avg(student):
    sum = 0
    count = 0
    grade_dict = get_grades(student)
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
def display_name_id_avg(student):
    avg = calculate_avg(student)
    #print students_to_ids["TOKiMONSTA"]
    id = students_to_ids[student]
    #print student + ", " + id + ", " + avg
    print student,id,avg

'''
makes table of id and respective averages
'''
def make_averages_table():
    command = "CREATE TABLE peeps_avg( id INTEGER, average INTEGER )"
    c.execute(command)
    for id in ids_to_names:
        command = "INSERT INTO peeps_avg VALUES( " + str(id) + ", " + str(calculate_avg(ids_to_names[id])) + ")"
        c.execute(command)

'''
adds a course, a course grade, and the id of the student who took the course to the courses table
also updates names_to_grades dictionary
'''
def add_courses(code , mark , id):
    code += " " #adds trailing space which other courses also have
    command = "INSERT INTO courses VALUES (\"" + code + "\", " + str(mark) +  ", " + str(id) + ")"
    c.execute(command)
    global names_to_grades #global allows us to reassign global variable
    names_to_grades = make_names_to_grades_dict()

'''
recalculates average for a student after more of their classes have been added in
'''
def update_avg(student):
    command = "UPDATE peeps_avg SET average = " + str(calculate_avg(student)) + " WHERE id = " + str(students_to_ids[student])
    c.execute(command)


#Do All of the initial stuff
populate()
names_to_grades = make_names_to_grades_dict()
ids_to_names = make_ids_to_names_dict()
students_to_ids = make_students_to_ids_dict()

print ""
print("***TEST Look up student grades***")
print("TOKiMONSTA: ")
print(get_grades("TOKiMONSTA"))
print("sasha: ")
print(get_grades("sasha"))
print("dorfmeister: ")
print(get_grades("dorfmeister"))
print("")

print("***TEST compute avg***")
print("TOKiMONSTA: ")
print(calculate_avg("TOKiMONSTA"))
print("digweed: ")
print(calculate_avg("digweed"))
print("dorfmeister: ")
print(calculate_avg("dorfmeister"))
print("")

print("***TEST display_name_id_avg")
print("tiesto: ")
display_name_id_avg("tiesto")
print("sasha: ")
display_name_id_avg("sasha")
print("dorfmeister: ")
display_name_id_avg("dorfmeister")
print("")

#Do all the updating stuff
make_averages_table()
add_courses("systems2", 85, 2)
add_courses("softdev2", 55, 4)
add_courses("WesternPoliticalTheory", 95, 5)
update_avg(ids_to_names[2])
update_avg(ids_to_names[4])
update_avg(ids_to_names[5])
db.commit() #save changes
db.close()  #close database
