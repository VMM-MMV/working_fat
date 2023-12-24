def building(building_name):
    timetable = "\n"
    timetable += f"""<Buildings_List>
    <Building>
        <Name>{building_name}</Name>
        <Comments></Comments>
    </Building>
    </Buildings_List>"""
    return timetable