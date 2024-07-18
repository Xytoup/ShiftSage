from datetime import timedelta

class Shift:
    def __init__(self, date, type):
        self.date = date
        self.type = type  # 'early', 'late', or 'night'
        self.duration = {'early': 7.5, 'late': 8.5, 'night': 9}[type]

    def __str__(self):
        return f"{self.type.capitalize()} Shift on {self.date} for {self.duration} hours"

def generate_shifts_for_month(workers, year, month, start_date, days_in_month):
    shifts_generated = []
    for day in range(days_in_month):
        date = start_date + timedelta(days=day)
        day_shifts = {'early': None, 'late': None, 'night': None}

        # Assign shifts to nurses based on their availability and workload constraints
        for shift_type in ['early', 'late', 'night']:
            shift_duration = get_shift_duration(shift_type)
            for nurse in workers:
                if can_work_shift(nurse, date, shift_type, shift_duration, shifts_generated):
                    nurse.add_shift(date, shift_type)  # Pass the shift type correctly
                    day_shifts[shift_type] = nurse.name
                    break
            if day_shifts[shift_type] is None:  # No available nurse was found for this shift
                day_shifts[shift_type] = "No Caretaker available"

        shifts_generated.append((date, day_shifts))
    return shifts_generated

def can_work_shift(nurse, date, shift_type, shift_duration, shifts_generated):
    # Check if the nurse has shifts that day already
    if any(shift.date == date for shift_list in nurse.shifts.values() for shift in shift_list):
        return False  # Can't work more than one shift per day

    # Check for 24 hours off after three consecutive night shifts
    if shift_type == 'early' and nurse.consecutive_night_shifts_ending(date - timedelta(days=1)) >= 3:
        return False  # Must have 24 hours off

    # Prevent early shift after a late shift the previous day
    if shift_type == 'early' and nurse.had_shift(date - timedelta(days=1), 'late'):
        return False

    # Ensure working hours do not exceed monthly limit
    projected_hours = nurse.get_monthly_hours(date.year, date.month) + shift_duration
    if projected_hours > (nurse.workload / 100) * (39.5 * 4):
        return False  # Exceeds monthly work hours

    return True

def get_shift_duration(shift_type):
    shift_durations = {'early': 7.5, 'late': 8.5, 'night': 9}
    return shift_durations.get(shift_type, 0)
