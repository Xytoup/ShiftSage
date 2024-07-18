import dearpygui.dearpygui as dpg
import calendar
from datetime import datetime
from shifts import generate_shifts_for_month
from src.database import load_workers_from_json

# Initialize global variables for current month and year
current_month = datetime.now().month
current_year = datetime.now().year


def setup_planning_view():
    global current_month, current_year

    with dpg.group(horizontal=True):
        dpg.add_button(label="Edit", tag="edit_button")
        dpg.add_button(label="Generate", tag="generate_button", callback=generate_button_callback)
        dpg.add_button(label="Export as Image", tag="export_button")
        dpg.add_button(label="Last Month", callback=lambda: change_month("prev"))
        dpg.add_button(label="Next Month", callback=lambda: change_month("next"))

    draw_calendar(current_month, current_year)


def generate_button_callback(sender, app_data, user_data):
    workers = load_workers_from_json('data/workers.json')
    days_in_month = calendar.monthrange(current_year, current_month)[1]
    current_date = datetime(current_year, current_month, 1)
    shifts_generated = generate_shifts_for_month(workers, current_year, current_month, current_date, days_in_month)
    display_shifts(shifts_generated, workers)


def draw_calendar(month, year):
    if dpg.does_item_exist("calendar"):
        dpg.delete_item("calendar")

    with dpg.child_window(tag="calendar", width=-1, height=-1, autosize_x=True, autosize_y=True):
        cal = calendar.Calendar(firstweekday=calendar.MONDAY)
        month_name = calendar.month_name[month]
        dpg.add_text(f"{month_name} {year}", color=[255, 255, 255, 255])

        with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True,
                       borders_outerV=True, row_background=True):
            days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            for day in days_of_week:
                dpg.add_table_column(label=day)

            for week in cal.monthdayscalendar(year, month):
                with dpg.table_row():
                    for day in week:
                        with dpg.table_cell():
                            if day != 0:
                                with dpg.group(horizontal=False):
                                    dpg.add_text(f"Day {day}", color=[150, 150, 250, 255])
                                    dpg.add_text("Early: TBD", tag=f"early_{year}_{month}_{day}",
                                                 color=[255, 255, 255, 255])
                                    dpg.add_text("Late: TBD", tag=f"late_{year}_{month}_{day}",
                                                 color=[255, 255, 255, 255])
                                    dpg.add_text("Night: TBD", tag=f"night_{year}_{month}_{day}",
                                                 color=[255, 255, 255, 255])
                            else:
                                dpg.add_text(" ")


def change_month(direction):
    global current_month, current_year

    if direction == "prev":
        if current_month == 1:
            current_month = 12
            current_year -= 1
        else:
            current_month -= 1
    elif direction == "next":
        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1

    draw_calendar(current_month, current_year)


def display_shifts(shifts_generated, workers):
    worker_dict = {worker.name: worker.qualified for worker in workers}

    for date, shifts in shifts_generated:
        day = date.day
        for shift_type, caretaker in shifts.items():
            cell = f"{shift_type}_{date.year}_{date.month}_{day}"
            if dpg.does_item_exist(cell):
                dpg.set_value(cell, f"{shift_type.capitalize()}: {caretaker}")
                if caretaker == "No Caretaker available":
                    dpg.configure_item(cell, color=[255, 0, 0, 255])
                else:
                    caretaker_color = [255, 255, 255, 255] if worker_dict[caretaker] else [128, 128, 128, 255]
                    dpg.configure_item(cell, color=caretaker_color)
