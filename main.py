from rooms_list import rooms
from time_constarints import time_constarints
from space_constaraints import space_constraints
from buildings_list import building
from hours import hours
from days import days
from activity_tag import activity_tag
from hackathon import preprocess

timetable = """﻿<?xml version="1.0" encoding="UTF-8"?>

<fet version="6.14.1">

<Mode>Official</Mode>

<Institution_Name>UTM</Institution_Name>

<Comments>Default comments</Comments>"""

activity, students, courses, teachers = preprocess() 
timetable += days()
timetable += hours()
timetable += courses
timetable += activity_tag()
timetable += teachers
timetable += students
timetable += activity

building_name = "FCIM"
timetable += building(building_name)
timetable += rooms(building_name)
timetable += time_constarints()
timetable += space_constraints()
timetable += "</fet>"

with open("work_pidar.fet", "w+",encoding="UTF-8") as f:
    f.write(timetable)