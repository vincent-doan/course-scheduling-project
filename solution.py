from datareader import *
import csv

class Solution:
    @staticmethod
    def get_next_slot(slot:tuple, idx:int) -> tuple:
            x = slot[1] + idx
            return ((slot[0], x, slot[2]))
    
    def __init__(self, path_to_all_courses:str="data/all_courses.csv", output_path:str="output/output.csv"):
        self.input_reader = InputReader(path_to_all_courses=path_to_all_courses)
        self.output_path = output_path
        self.N = self.input_reader.get_num_courses()
        self.M = self.input_reader.get_num_classrooms()

        self.courses_info = self.input_reader.get_formatted_courses_info()
        self.professors_list = self.input_reader.get_professors_list()
        self.classrooms_list = self.input_reader.get_classrooms_list()
        self.classroom_seats = self.input_reader.get_classroom_seats()

        self.all_slots = [(session, period, classroom) for classroom in self.classrooms_list for session in range(10) for period in range(6)]
        self.timetable = [(None, None, None)] * self.N
        self.solution_obtained = False

    # ----------------- Helper functions -----------------
    def num_periods(self, course:int) -> int: 
        return self.courses_info[course][0]
    def professor(self, course:int) -> int:
        return self.courses_info[course][1]
    def num_students(self, course:int) -> int:
        return self.courses_info[course][2]
    def capacity(self, classroom:int) -> int:
        return self.classroom_seats[classroom]
    
    # ----------------- Export output to csv -----------------
    def export_timetable(self) -> None:
        with open(self.output_path, 'w', newline='') as fp:
            timetable_sorted = list()
            for idx, slot in enumerate(self.timetable):
                timetable_sorted.append((slot[0], slot[1], slot[2], idx))
            
            timetable_sorted.sort(key=lambda t: (t[0], t[2], t[1], t[3]))
            
            csv_writer = csv.writer(fp, delimiter=',')
            csv_writer.writerow(['Faculty', 'Class ID', 'Course ID', 'Course Name', 'Credits', 'Num. Students', 'Num. Periods', 'Professor', 'Session', 'Start', 'End', 'Classroom', 'Capacity'])
            for (session, period, classroom, course) in timetable_sorted:
                course_info = list(self.input_reader.idx_to_course_info(course).values())
                course_info.append(self.input_reader.convert_session(session))
                course_info.append(period)
                course_info.append(period + self.num_periods(course) - 1)
                course_info.append(self.input_reader.idx_to_classroom_id(classroom))
                course_info.append(self.capacity(classroom))
                csv_writer.writerow(course_info)

    # ----------------- Condition checking functions -----------------
    def not_enough_periods_left(self, course:int, slot:tuple) -> bool:
        if (6 - slot[1]) < self.num_periods(course): 
            return True
        return False

    def slot_is_taken(self, course:int, slot:tuple) -> bool:
        for (index, assigned_slot) in enumerate(self.timetable[:course]): 
            for i in range(self.num_periods(course)):
                for j in range(self.num_periods(index)):
                    if Solution.get_next_slot(slot, i) == Solution.get_next_slot(assigned_slot, j): 
                        return True
        return False

    def not_enough_capacity(self, course:int, slot:tuple) -> bool:
        if self.capacity(slot[2]) < self.num_students(course):
            return True
        return False

    def has_prof_duplicate(self, course:int, slot:tuple) -> bool:
        periods_covered_by_course = {(slot[1] + i) for i in range(self.num_periods(course))}
        for index, assigned_slot in enumerate(self.timetable[:course]): 
            assigned_course = index
            periods_covered_by_assigned_course = {(assigned_slot[1] + j) for j in range(self.num_periods(assigned_course))}
            if self.professor(course) == self.professor(assigned_course) and slot[0] == assigned_slot[0]:
                if len(periods_covered_by_course & periods_covered_by_assigned_course) != 0:
                    return True
        return False

    # ----------------- To be overwritten -----------------
    def get_solution(self) -> None:
        pass