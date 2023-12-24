import pandas as pd
from prettytable import PrettyTable

def time_constarints():
    profesors = pd.read_csv("Groups and Subjects (FAF Hack) - Profesori.csv")
    subjects = pd.read_csv("Groups and Subjects (FAF Hack) - Subiecte.csv")

    profesors = pd.merge(profesors, subjects,left_on='subject', right_on='id', how='left').drop('id_y',axis=1)

    profesors = profesors[profesors['semestru'] == 1]
    profesors = profesors = profesors[profesors['type'] != 'LAB']
    profesors = profesors.drop_duplicates(subset='unitate_curs')
    

    period_columns = [
        'mon_per_1', 'mon_per_2', 'mon_per_3', 'mon_per_4', 'mon_per_5', 'mon_per_6', 'mon_per_7',
        'tue_per_1', 'tue_per_2', 'tue_per_3', 'tue_per_4', 'tue_per_5', 'tue_per_6', 'tue_per_7',
        'wed_per_1', 'wed_per_2', 'wed_per_3', 'wed_per_4', 'wed_per_5', 'wed_per_6', 'wed_per_7',
        'thu_per_1', 'thu_per_2', 'thu_per_3', 'thu_per_4', 'thu_per_5', 'thu_per_6', 'thu_per_7',
        'fri_per_1', 'fri_per_2', 'fri_per_3', 'fri_per_4', 'fri_per_5', 'fri_per_6', 'fri_per_7',
        'sat_per_1', 'sat_per_2', 'sat_per_3', 'sat_per_4', 'sat_per_5', 'sat_per_6', 'sat_per_7'
    ]

    # Add up all the period columns to create 'availability'
    profesors['availability'] = profesors[period_columns].sum(axis=1)

    maximum_availability = 42 # hours

    timetable = "\n"
    timetable += """<Time_Constraints_List>
    <ConstraintBasicCompulsoryTime>
        <Weight_Percentage>100</Weight_Percentage>
        <Active>true</Active>
        <Comments></Comments>
    </ConstraintBasicCompulsoryTime>"""


    days = {"mon": "Monday", "tue": "Tuesday", "wed" : "Wednesday", "thu" : "Thursday", "fri" : "Friday", "sat" : "Saturday"}
    hours = {"1": "08:00-9:30", "2": "09:45-11:15", "3": "11:30-13:00", "4": "13:30-15:00", "5": "15:15-16:45", "6": "17:00-18:30", "7": "18:45-20:15"}

    for i in range(len(profesors)):
        profesor_name = profesors.iloc[i, 1]
        nr_not_available = maximum_availability - profesors.iloc[i, len(profesors.columns)-1]

        timetable += "\n"
        timetable += f"""<ConstraintTeacherNotAvailableTimes>
        <Weight_Percentage>100</Weight_Percentage>
        <Teacher>{profesor_name}</Teacher>
        <Number_of_Not_Available_Times>{nr_not_available}</Number_of_Not_Available_Times>"""
        for j in range(len(profesors.iloc[i])):
            cell_value = profesors.iloc[i, j]
            column_name = profesors.columns[j]
            if (cell_value == 0) and (column_name[:3] in list(days.keys())):
                timetable += "\n"
                timetable += f"""<Not_Available_Time>
                        <Day>{days[column_name[:3]]}</Day>
                        <Hour>{hours[column_name[-1]]}</Hour>
                    </Not_Available_Time>"""
        
        timetable += "\n"
        timetable += """<Active>true</Active>
        <Comments></Comments>
        </ConstraintTeacherNotAvailableTimes>"""
                
    timetable += "\n"
    timetable += "</Time_Constraints_List>"
    return timetable

if __name__ == "__main__":
    time_constarints()