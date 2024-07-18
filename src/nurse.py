import json
import random
from datetime import timedelta
from shifts import Shift

class Nurse:
    def __init__(self, qualified, name, workload, max_nightshifts_month, max_consecutive_nightshifts, id=None):
        self.id = id if id else Nurse.generate_unique_id()
        self.qualified = qualified
        self.name = name
        self.workload = workload
        self.max_nightshifts_month = max_nightshifts_month
        self.max_consecutive_nightshifts = max_consecutive_nightshifts
        self.shifts = {}  # Dictionary to store shifts by date

    def add_shift(self, shift_date, shift_type):
        new_shift = Shift(shift_date, shift_type)
        if shift_date in self.shifts:
            self.shifts[shift_date].append(new_shift)
        else:
            self.shifts[shift_date] = [new_shift]

    def get_monthly_hours(self, year, month):
        total_hours = 0
        for shift_list in self.shifts.values():
            for shift in shift_list:
                if shift.date.year == year and shift.date.month == month:
                    total_hours += shift.duration
        return total_hours

    def consecutive_night_shifts_ending(self, end_date):
        count = 0
        current_date = end_date
        while current_date in self.shifts:
            if any(shift.type == 'night' for shift in self.shifts[current_date]):
                count += 1
                current_date -= timedelta(days=1)
            else:
                break
        return count

    def had_shift(self, check_date, shift_type):
        if check_date in self.shifts:
            return any(shift.type == shift_type for shift in self.shifts[check_date])
        return False

    def to_dict(self):
        return {
            'id': self.id,
            'qualified': self.qualified,
            'name': self.name,
            'workload': self.workload,
            'max_nightshifts_month': self.max_nightshifts_month,
            'max_consecutive_nightshifts': self.max_consecutive_nightshifts
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            qualified=data['qualified'],
            name=data['name'],
            workload=data['workload'],
            max_nightshifts_month=data['max_nightshifts_month'],
            max_consecutive_nightshifts=data['max_consecutive_nightshifts'],
            id=data['id']
        )

    @staticmethod
    def generate_unique_id():
        existing_ids = Nurse.load_existing_ids()
        while True:
            new_id = random.randint(1000, 9999)
            if new_id not in existing_ids:
                existing_ids.add(new_id)
                Nurse.save_existing_ids(existing_ids)
                return new_id

    @staticmethod
    def load_existing_ids():
        try:
            with open('data/used_ids.json', 'r') as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()

    @staticmethod
    def save_existing_ids(ids):
        with open('data/used_ids.json', 'w') as f:
            json.dump(list(ids), f)
