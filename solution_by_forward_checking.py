from solution import Solution

class SolutionByForwardChecking(Solution):
    def get_solution(self) -> None:
        
        slots_for_all_courses = [list(self.all_slots) for _ in range(self.N)]
        for all_slots in slots_for_all_courses:
            for slot in list(all_slots):
                if self.capacity(slot[2]) < self.num_students(slots_for_all_courses.index(all_slots)):
                    all_slots.remove(slot)

        def pass_forward_check(course, latest_assigned_course):
            latest_assigned_slot = self.timetable[latest_assigned_course]
            slots_covered = [Solution.get_next_slot(latest_assigned_slot, i) for i in range(self.num_periods(latest_assigned_course))]
            deleted_slots = list()
            if self.professor(course) == self.professor(latest_assigned_course):
                for slot in slots_covered:
                    if slot in slots_for_all_courses[course]:
                        slots_for_all_courses[course].remove(slot)
                        deleted_slots.append(slot)
            if (5 - latest_assigned_slot[1] - self.num_periods(latest_assigned_course)) < self.num_periods(course):
                for i in range(1, 5 - latest_assigned_slot[1] + 1):
                    slot = Solution.get_next_slot(latest_assigned_slot, i)
                    if slot in slots_for_all_courses[course]:
                        slots_for_all_courses[course].remove(slot)
                        deleted_slots.append(slot)
            if len(slots_for_all_courses[course]) > 0:
                return True, deleted_slots
            else:
                return False, deleted_slots

        def assign(course):
            print("Assigning course", course + 1, "/", self.N)
            # failed_slots = list()
            for slot in list(slots_for_all_courses[course]):
                if self.solution_obtained == True:
                    return
                
                # if slot in failed_slots:
                #     continue
                
                self.timetable[course] = slot

                # Remove the assigned slot from all domains
                for i in range(self.num_periods(course)):
                    for all_slots in slots_for_all_courses:
                        if Solution.get_next_slot(slot, i) in all_slots:
                            all_slots.remove(Solution.get_next_slot(slot, i))

                # Apply forward checking
                for course_to_check in range(course + 1, self.N):
                    pass_check, deleted_slots = pass_forward_check(course_to_check, latest_assigned_course=course)
                    if not pass_check:
                        slots_for_all_courses[course].extend(deleted_slots)
                        # failed_slots.append(slot)
                        return

                if course == self.N - 1:
                    self.export_timetable()
                    self.solution_obtained = True
                else:
                    assign(course + 1)
                
        assign(0)