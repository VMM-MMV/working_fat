import pandas as pd


def rooms(building):
    cabinets = pd.read_csv("Groups and Subjects (FAF Hack) - Cabinete.csv") 

    third_column_name = cabinets.columns[2]

    cabinets_cleaned = cabinets.dropna(subset=[third_column_name])

    timetable = "\n"
    timetable += "<Rooms_List>"
    for i in range(len(cabinets_cleaned)):
        cabinet_name = cabinets_cleaned.iloc[i, 0]
        capacity = int(cabinets_cleaned.iloc[i, 2])
        timetable += "\n"
        timetable += f"""<Room>
            <Name>{cabinet_name}</Name>
            <Building>{building}</Building>
            <Capacity>{capacity}</Capacity>
            <Virtual>false</Virtual>
            <Comments></Comments>
        </Room>"""
    timetable += "\n"
    timetable += "</Rooms_List>"
    return timetable

if __name__ == "__main__":
    print(rooms("FCIM"))
        
