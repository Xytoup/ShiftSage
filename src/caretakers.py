from nurse import Nurse
from database import load_workers_from_json, save_workers_to_json
import dearpygui.dearpygui as dpg

def add_worker(sender, app_data, user_data):
    with dpg.window(label="Add New Worker", modal=True, tag="add_worker_modal", width=600, height=200):
        dpg.add_checkbox(label="Qualified Nurse", tag="input_qualified")
        dpg.add_input_text(label="Name", tag="input_name")
        dpg.add_input_text(label="Workload in %", tag="input_workload")
        dpg.add_input_text(label="Max Nightshifts per Month", tag="input_max_nightshifts_month")
        dpg.add_input_text(label="Max Consecutive Nightshifts", tag="input_max_consecutive_nightshifts")
        dpg.add_button(label="Submit", callback=submit_new_worker)
        dpg.add_button(label="Cancel", callback=lambda: dpg.delete_item("add_worker_modal"))

def submit_new_worker(sender, app_data, user_data):
    qualified = dpg.get_value("input_qualified")
    name = dpg.get_value("input_name")
    workload = int(dpg.get_value("input_workload"))
    max_nightshifts_month = int(dpg.get_value("input_max_nightshifts_month"))
    max_consecutive_nightshifts = int(dpg.get_value("input_max_consecutive_nightshifts"))

    workers = load_workers_from_json('data/workers.json')

    new_worker = Nurse(qualified, name, workload, max_nightshifts_month, max_consecutive_nightshifts)
    workers.append(new_worker)
    save_workers_to_json(workers, 'data/workers.json')
    dpg.delete_item("add_worker_modal")
    populate_caretakers_window()  # Refresh the display

def delete_worker(sender, app_data, user_data):
    workers = load_workers_from_json('data/workers.json')
    if workers:
        with dpg.window(label="Delete Worker", modal=True, tag="delete_worker_modal", width=400, height=800):
            for worker in workers:
                dpg.add_button(label=f"Delete {worker.name}", callback=confirm_delete_worker, user_data=worker.id)
    else:
        print("No workers to delete.")

def confirm_delete_worker(sender, app_data, user_data):
    worker_id = user_data  # Retrieve the worker ID from user_data
    print(f"Attempting to delete worker with ID: {worker_id}")
    workers = load_workers_from_json('data/workers.json')
    workers_before = len(workers)
    workers = [w for w in workers if w.id != worker_id]  # Remove the worker by filtering the list
    workers_after = len(workers)
    print(f"Workers before deletion: {workers_before}, after deletion: {workers_after}")
    save_workers_to_json(workers, 'data/workers.json')
    dpg.delete_item("delete_worker_modal")
    populate_caretakers_window()  # Refresh the display

def edit_worker(sender, app_data, user_data):
    print("Edit worker button clicked")

def populate_caretakers_window():
    workers = load_workers_from_json('data/workers.json')
    if dpg.does_item_exist("caretakers_table"):
        dpg.delete_item("caretakers_table")

    with dpg.child_window(tag="caretakers_table", parent="caretakers_view", width=-1, height=-1):
        # Create themes for green and red text
        with dpg.theme() as green_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [0, 255, 0, 255])  # Green text

        with dpg.theme() as red_theme:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 0, 0, 255])  # Red text

        # Create themes for each button
        with dpg.theme() as add_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [106, 191, 89, 255])  # Green for add

        with dpg.theme() as delete_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [191, 89, 89, 255])  # Red for delete

        with dpg.theme() as edit_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, [190, 190, 80, 255])  # Yellow for edit

        # Buttons for actions
        with dpg.group(horizontal=True):
            add_button = dpg.add_button(label="Add Caretaker", tag="add_worker_button", callback=add_worker)
            dpg.bind_item_theme(add_button, add_theme)

            delete_button = dpg.add_button(label="Delete Caretaker", tag="delete_worker_button", callback=delete_worker)
            dpg.bind_item_theme(delete_button, delete_theme)

            edit_button = dpg.add_button(label="Edit Caretaker", tag="edit_worker_button", callback=edit_worker)
            dpg.bind_item_theme(edit_button, edit_theme)

        if not workers:
            dpg.add_text("No caretakers found.", parent="caretakers_table")
        else:
            for worker in workers:
                if worker.qualified:
                    text = dpg.add_text(f"Nurse - {worker.name}", parent="caretakers_table")
                    dpg.bind_item_theme(text, green_theme)
                else:
                    text = dpg.add_text(f"Assistant - {worker.name}", parent="caretakers_table")
                    dpg.bind_item_theme(text, red_theme)

                dpg.add_text(f"ID: {worker.id}, Workload: {worker.workload}%, Max Nightshifts/Month: {worker.max_nightshifts_month}, Max Consecutive Nightshifts: {worker.max_consecutive_nightshifts}", parent="caretakers_table")
