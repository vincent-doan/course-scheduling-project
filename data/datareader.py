import pandas as pd

class InputReader:

    sessions_dic = dic = {0:"Monday morning", 
                        1:"Monday afternoon", 
                        2:"Tuesday morning", 
                        3:"Tuesday afternoon",
                        4:"Wednesday morning",
                        5:"Wednesday afternoon",
                        6:"Thursday morning",
                        7:"Thursday afternoon",
                        8:"Friday morning",
                        9:"Friday afternoon"}
    
    def __init__(self,
                 path_to_all_professors:str="data/all_professors.csv",
                 path_to_all_courses:str="data/all_courses.csv",
                 path_to_all_classrooms:str="data/all_classrooms.csv") -> None:
        
        # Read all professors
        self.all_professors_df = pd.read_csv(path_to_all_professors)
        self.all_professors_dic = self.all_professors_df.to_dict()
    
        # Read all courses
        self.all_courses_df = pd.read_csv(path_to_all_courses)
        self.all_courses_dic = dict()
        for index, row in self.all_courses_df.iterrows():
            row = row[1:]
            self.all_courses_dic[index] = row.to_dict()

        # Read all classrooms
        self.all_classrooms_df = pd.read_csv(path_to_all_classrooms)
        self.all_classrooms_dic = dict()
        for index, row in self.all_classrooms_df.iterrows():
            row = row[1:]
            self.all_classrooms_dic[index] = row.to_dict()

    # --------------------------------------------------
    def get_num_courses(self) -> int:
        return self.all_courses_df.shape[0]
    def get_num_classrooms(self) -> int:
        return self.all_classrooms_df.shape[0]

    # --------------------------------------------------
    def convert_session(self, idx:int) -> str:
        return InputReader.sessions_dic[idx]
    def idx_to_prof_id(self, idx:int) -> str:
        return self.all_professors_dic["Professor ID"][idx]
    def prof_id_to_idx(self, prof_id:str) -> int:
        return int(prof_id[4:])
    def idx_to_course_info(self, idx:int) -> dict:
        return self.all_courses_dic[idx]
    def idx_to_classroom_id(self, idx:int) -> dict:
        return self.all_classrooms_dic[idx]['Classroom']

    # --------------------------------------------------
    def get_formatted_courses_info(self) -> dict:
        courses_info = dict()
        for idx in range(self.get_num_courses()):
            all_info = self.all_courses_dic[idx]
            courses_info[idx] = (all_info['Num. Periods'], self.prof_id_to_idx(all_info['Professor']), all_info['Num. Students'])
        return courses_info

    def get_professors_list(self) -> list:
        return list(map(self.prof_id_to_idx, self.all_courses_df['Professor'].unique().tolist()))

    def get_classrooms_list(self) -> list:
        return list(range(0, self.get_num_classrooms()))

    def get_classroom_seats(self) -> list:
        return self.all_classrooms_df['Capacity'].tolist()