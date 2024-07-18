from caretakers import populate_caretakers_window
from planning import draw_calendar, change_month
import dearpygui.dearpygui as dpg
import datetime

from planning import setup_planning_view

def interface_loop():
    dpg.create_context()
    dpg.create_viewport(title='ShiftSage v1.0.0-alpha', width=1920, height=1080)

    with dpg.window(label="Main Window", width=1920, height=1080):
        dpg.add_button(label="Caretakers", callback=lambda: toggle_windows("caretakers_view"))
        dpg.add_button(label="Planning", callback=lambda: toggle_windows("planning_view"))

        with dpg.child_window(tag="caretakers_view", width=1920, height=1080, show=True):
            populate_caretakers_window()

        with dpg.child_window(tag="planning_view", width=1920, height=1080, show=False):
            setup_planning_view()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

def toggle_windows(view_to_show):
    dpg.configure_item("caretakers_view", show=(view_to_show == "caretakers_view"))
    dpg.configure_item("planning_view", show=(view_to_show == "planning_view"))

if __name__ == "__main__":
    interface_loop()
