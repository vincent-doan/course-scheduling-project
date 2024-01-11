from solution import Solution

class SolutionByValueOrdering(Solution):
    def get_solution(self) -> None:

        def update_all_slots(course):
            temp = list(self.all_slots)
            
            classrooms_with_enough_capacity = list()
            for idx, capacity in enumerate(self.classroom_seats):
                if capacity >= self.num_students(course):
                    classrooms_with_enough_capacity.append(idx)
            
            updated_all_slots = [x for x in temp if x[2] in classrooms_with_enough_capacity]
            updated_all_slots.sort(key = lambda t: self.capacity(t[2]))
            return updated_all_slots

        def assign(course):
            print("Assigning course", course + 1, "/", self.N)
            failed_slots = list()
            for slot in update_all_slots(course):
                if self.solution_obtained == True:
                    return
                
                if slot in failed_slots:
                    continue
                if self.not_enough_periods_left(course, slot):
                    continue
                if self.slot_is_taken(course, slot):
                    continue
                if self.not_enough_capacity(course, slot):
                    continue
                if self.has_prof_duplicate(course, slot):
                    continue
            
                self.timetable[course] = slot
                # Remove the assigned slot from self.all_slots
                for i in range(self.num_periods(course)):
                    self.all_slots.remove(Solution.get_next_slot(slot, i)) 

                if course == self.N - 1:
                    self.export_timetable()
                    self.solution_obtained = True
                else:
                    assign(course + 1)

                # Re-add the slot to self.all_slots when backtracking
                if not self.solution_obtained:
                    for i in range(self.num_periods(course)):
                        self.all_slots.append(Solution.get_next_slot(slot, ))
                    failed_slots.append(slot)
            
        assign(0)