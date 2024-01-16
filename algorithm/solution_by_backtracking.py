from .solution import Solution

class SolutionByBacktracking(Solution):
    def get_solution(self) -> None:

        def assign(course):
            print("Assigning course", course + 1, "/", self.N)
            # Create a copy of self.all_slots for iteration
            for slot in list(self.all_slots):
                if self.solution_obtained == True:
                    return
                
                if self.not_enough_capacity(course, slot):
                    continue
                if self.not_enough_periods_left(course, slot):
                    continue
                if self.slot_is_taken(course, slot):
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
                        self.all_slots.append(Solution.get_next_slot(slot, i))

        assign(0)