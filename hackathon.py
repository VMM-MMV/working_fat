import pandas as pd
import numpy as np
import re

def preprocess():
    subjects = pd.read_csv("Groups and Subjects (FAF Hack) - Subiecte.csv")
    cabinets = pd.read_csv("Groups and Subjects (FAF Hack) - Cabinete.csv")
    groups = pd.read_csv("Groups and Subjects (FAF Hack) - Grupe.csv")
    profesors = pd.read_csv("Groups and Subjects (FAF Hack) - Profesori.csv")

    subjects.TOTAL.isna().value_counts()
    subjects.TOTAL.isna()
    nas=subjects['TOTAL'].isna()
    for i in range(len(nas)):
        if nas[i] ==  False:
            subjects['lab'][i]=subjects['TOTAL'][i].split(" ")[1]
    subjects=subjects.drop(['TOTAL','anul'],axis=1)


    merged_table = pd.merge(profesors, subjects,left_on='subject', right_on='id', how='left').drop('id_y',axis=1)
    merged_table = merged_table[merged_table['semestru'] == 1]
   


    def teachers():
        teachers_fet="<Teachers_List>\n"
        for i in range(len(merged_table)):
            prof = merged_table.iloc[i] 
            print(prof["unitate_curs"])
            # print(prof)
            teacher=f"""
            <Teacher>
                <Name>{prof['name']}</Name>
                <Target_Number_of_Hours>0</Target_Number_of_Hours>
                <Qualified_Subjects>
                    <Qualified_Subject>{prof['unitate_curs']}</Qualified_Subject>
                </Qualified_Subjects>
                <Comments></Comments>
            </Teacher>"""
            teachers_fet+=teacher
        teachers_fet+="\n</Teachers_List>"

        return teachers_fet

    def courses():
        subjects_fet="<Subjects_List>\n"
        for i in range(len(merged_table)):
            prof = merged_table.iloc[i] 
            # print(prof)
            subject=f"""
            <Subject>
                <Name>{prof['unitate_curs']}</Name>
                <Comments></Comments>
            </Subject>"""
            subjects_fet+=subject
        subjects_fet+="\n</Subjects_List>"

        return subjects_fet

    def activity():
        joint_table = pd.DataFrame()

        for i in range(len(groups)):
            group = groups.iloc[i] 
            formatted_subjects=[int(x) for x in group['subject_ids'].replace(" ","").split(",") if x!='']
            joint_table_data = []
            group['subject_ids'] = formatted_subjects
            df_explode = group.explode('subject_ids').to_frame()
            for subj_id in formatted_subjects:
                joint_table_data.append(({'id': group['id'], 'subject_id': subj_id}))
            joint_table = pd.concat([joint_table,pd.DataFrame(joint_table_data)])
        joint_table
        # make joint table

        activity_fet="\n<Activities_List>\n"
        activity_id=1
        for i in range(len(merged_table)):
            prof = merged_table.iloc[i] 
            joint = joint_table[joint_table.subject_id==prof.subject]
            lesson = prof.unitate_curs
            group_ids = joint['id']
            subject_ids = prof.subject
            group_names = [groups[groups['id']==x]['speciality'].values[0] for x in group_ids]

            for j in range(len(group_names)):
                lecture_type = 'Lab' if prof['type']=='LAB' else 'Lectures'
                activity=f"""
        <Activity>
            <Teacher>{prof['name']}</Teacher>
            <Subject>{lesson}</Subject>
            <Activity_Tag>{lecture_type}</Activity_Tag>
            <Students>{group_names[j]}</Students>
            <Duration>1</Duration>
            <Total_Duration>1</Total_Duration>
            <Id>{activity_id}</Id>
            <Activity_Group_Id>0</Activity_Group_Id>
            <Active>true</Active>
            <Comments></Comments>
        </Activity>"""
                activity_fet+=activity
                activity_id+=1
        activity_fet+="\n</Activities_List>"

        return activity_fet

    def students():
        students_fet="<Students_List>\n"
        students_fet += f"""
        <Year>
            <Name>1st</Name>
            <Number_of_Students>{groups['nr_persoane'].sum()}</Number_of_Students>
            <Comments></Comments>
            <Number_of_Categories>0</Number_of_Categories>
            <Separator> </Separator>
            """

        for i in range(len(groups)):
            group = groups.iloc[i] 
            if "22" not in group.speciality:
                subject=f"""
                <Group>
                    <Name>{group.speciality}</Name>
                    <Number_of_Students>{group.nr_persoane}</Number_of_Students>
                    <Comments></Comments>
                </Group>"""
                students_fet+=subject
        students_fet+="\n</Year>\n</Students_List>"

        return students_fet
    return activity(),students(),courses(),teachers()

if __name__ == "__main__":
    preprocess()