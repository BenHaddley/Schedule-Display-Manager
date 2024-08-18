import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from PIL import Image, ImageTk
import os
import datetime
import pytz
from generate_slides import generate_slides

class CheatSheetApp:
    def __init__(self, root, secondary_root):
        self.root = root
        self.secondary_root = secondary_root

        self.setup_styles()
        self.setup_cheat_sheet()
        self.setup_presentation()

    def setup_styles(self):
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 10), padding=10, background='blue', foreground='black')
        style.map('TButton', background=[('active', 'blue'), ('disabled', 'grey')])
        style.configure('TLabel', font=('Helvetica', 12), padding=5)
        style.configure('TEntry', font=('Helvetica', 12))
        style.configure('TText', font=('Helvetica', 12))

    def setup_cheat_sheet(self):
        self.root.title("Cheat Sheet")
        self.root.geometry("800x450")
        self.root.configure(bg='#f0f0f0')

        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.cheat_sheet_text = tk.Text(self.root, wrap=tk.WORD, font=('Helvetica', 12), bg='#ffffff', fg='#000000', padx=10, pady=10)
        self.cheat_sheet_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.save_button = ttk.Button(left_frame, text="Save and Update Slides", command=self.save_and_update_slides)
        self.save_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.add_course_button = ttk.Button(left_frame, text="Add Course", command=self.add_course)
        self.add_course_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.add_appointment_button = ttk.Button(left_frame, text="Add Appointment", command=self.add_appointment)
        self.add_appointment_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.delete_course_button = ttk.Button(left_frame, text="Delete Course", command=self.delete_course)
        self.delete_course_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.delete_appointment_button = ttk.Button(left_frame, text="Delete Appointment", command=self.delete_appointment)
        self.delete_appointment_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.edit_course_button = ttk.Button(left_frame, text="Edit Course", command=self.edit_course)
        self.edit_course_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.edit_appointment_button = ttk.Button(left_frame, text="Edit Appointment", command=self.edit_appointment)
        self.edit_appointment_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.refresh_button = ttk.Button(left_frame, text="Refresh Data", command=self.refresh_data)
        self.refresh_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.help_button = ttk.Button(left_frame, text="Help", command=self.show_help)
        self.help_button.pack(side=tk.TOP, padx=5, pady=5, fill=tk.X)

        self.load_cheat_sheet()

    def load_cheat_sheet(self):
        try:
            with open("slides/cheat_sheet.txt", "r") as file:
                self.cheat_sheet_text.delete("1.0", tk.END)
                self.cheat_sheet_text.insert(tk.END, file.read())
        except FileNotFoundError:
            with open("slides/cheat_sheet.txt", "w") as file:
                file.write("")
            self.cheat_sheet_text.delete("1.0", tk.END)

    def save_and_update_slides(self):
        with open("slides/cheat_sheet.txt", "w") as file:
            file.write(self.cheat_sheet_text.get("1.0", tk.END).strip())
        generate_slides()
        self.slides = [os.path.join("slides", slide) for slide in os.listdir("slides") if slide.endswith('.png')]
        self.current_slide = 0
        self.show_slide(self.current_slide)

    def add_course(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("New Course")
        new_window.configure(bg='#f0f0f0')
        new_window.geometry("600x400")

        frame = ttk.Frame(new_window)
        frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        ttk.Label(frame, text="Course Name").grid(row=0, column=0, pady=5, sticky='e')
        course_entry = ttk.Entry(frame)
        course_entry.grid(row=0, column=1, pady=5, sticky='w')

        ttk.Label(frame, text="Start Date").grid(row=1, column=0, pady=5, sticky='e')
        start_cal = Calendar(frame, selectmode='day', date_pattern='dd-mm-yyyy', background='#f0f0f0', foreground='#000000')
        start_cal.grid(row=1, column=1, pady=5, sticky='w')

        ttk.Label(frame, text="End Date").grid(row=1, column=2, pady=5, sticky='e')
        end_cal = Calendar(frame, selectmode='day', date_pattern='dd-mm-yyyy', background='#f0f0f0', foreground='#000000')
        end_cal.grid(row=1, column=3, pady=5, sticky='w')

        ttk.Label(frame, text="People on Course").grid(row=2, column=0, pady=5, sticky='ne')
        people_entry = tk.Text(frame, height=4, width=30, font=('Helvetica', 12), bg='#ffffff', fg='#000000')
        people_entry.grid(row=2, column=1, pady=5, sticky='w', columnspan=3)

        ttk.Label(frame, text="Details").grid(row=3, column=0, pady=5, sticky='ne')
        details_entry = tk.Text(frame, height=4, width=30, font=('Helvetica', 12), bg='#ffffff', fg='#000000')
        details_entry.grid(row=3, column=1, pady=5, sticky='w', columnspan=3)

        def save_course():
            course_name = course_entry.get().strip()
            start_date = start_cal.get_date()
            end_date = end_cal.get_date()
            people = people_entry.get("1.0", tk.END).strip()
            details = details_entry.get("1.0", tk.END).strip()

            if course_name and start_date and end_date and people and details:
                start_dtg = self.convert_to_dtg(start_date)
                end_dtg = self.convert_to_dtg(end_date)
                if start_dtg and end_dtg:
                    course_info = f"{course_name},{start_dtg},{end_dtg},{people},{details}"
                    content = self.cheat_sheet_text.get("1.0", tk.END)
                    if "Upcoming Courses:" in content:
                        parts = content.split("Upcoming Courses:")
                        new_content = parts[0] + "Upcoming Courses:\n" + course_info + "\n" + parts[1]
                    else:
                        new_content = "Upcoming Courses:\n" + course_info + "\n" + content
                    self.cheat_sheet_text.delete("1.0", tk.END)
                    self.cheat_sheet_text.insert(tk.END, new_content)

                    new_window.destroy()
                    self.save_and_update_slides()
                else:
                    messagebox.showerror("Error", "Invalid date format.")
            else:
                messagebox.showerror("Error", "All fields must be filled out")

        save_button = ttk.Button(frame, text="Save Course", command=save_course)
        save_button.grid(row=4, column=0, columnspan=4, pady=5)

    def add_appointment(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("New Appointment")
        new_window.configure(bg='#f0f0f0')

        frame = ttk.Frame(new_window)
        frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        ttk.Label(frame, text="Name").grid(row=0, column=0, pady=5)
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=0, column=1, pady=5)

        ttk.Label(frame, text="Type of Appointment").grid(row=1, column=0, pady=5)
        appointment_type_var = tk.StringVar(frame)
        appointment_types = ["Dental", "Physio", "Medical", "Other"]
        appointment_type_menu = ttk.OptionMenu(frame, appointment_type_var, *appointment_types)
        appointment_type_menu.grid(row=1, column=1, pady=5)

        custom_type_entry = ttk.Entry(frame)
        custom_type_entry.grid(row=1, column=2, pady=5)
        custom_type_entry.grid_remove()

        def update_custom_type_entry(*args):
            if appointment_type_var.get() == "Other":
                custom_type_entry.grid()
            else:
                custom_type_entry.grid_remove()

        appointment_type_var.trace("w", update_custom_type_entry)

        ttk.Label(frame, text="Date").grid(row=2, column=0, pady=5)
        cal = Calendar(frame, selectmode='day', date_pattern='dd-mm-yyyy', background='#f0f0f0', foreground='#000000')
        cal.grid(row=2, column=1, pady=5)

        ttk.Label(frame, text="Time (HH:MM)").grid(row=3, column=0, pady=5)
        time_entry = ttk.Entry(frame)
        time_entry.grid(row=3, column=1, pady=5)

        def save_appointment():
            name = name_entry.get().strip()
            appointment_type = appointment_type_var.get()
            if appointment_type == "Other":
                appointment_type = custom_type_entry.get().strip()
            date = cal.get_date()
            time = time_entry.get().strip()

            if name and appointment_type and date and time:
                dtg_date = self.convert_to_dtg(date, time)
                if dtg_date:
                    content = self.cheat_sheet_text.get("1.0", tk.END)
                    if "Appointments:" in content:
                        parts = content.split("Appointments:")
                        new_content = parts[0] + "Appointments:\n" + f"{name},{appointment_type},{dtg_date}\n" + parts[1]
                    else:
                        new_content = content + f"\nAppointments:\n{name},{appointment_type},{dtg_date}\n"
                    self.cheat_sheet_text.delete("1.0", tk.END)
                    self.cheat_sheet_text.insert(tk.END, new_content)

                    new_window.destroy()
                    self.save_and_update_slides()
                else:
                    messagebox.showerror("Error", "Invalid time format. Use HH:MM")
            else:
                messagebox.showerror("Error", "All fields must be filled out")

        save_button = ttk.Button(frame, text="Save Appointment", command=save_appointment)
        save_button.grid(row=4, columnspan=2, pady=5)

    def delete_course(self):
        content = self.cheat_sheet_text.get("1.0", tk.END)
        if "Upcoming Courses:" in content:
            parts = content.split("Upcoming Courses:")
            lines = parts[1].split('\n')
            if lines:
                lines.pop(0)  # Remove the first course
                parts[1] = '\n'.join(lines)
                new_content = parts[0] + "Upcoming Courses:" + parts[1]
                self.cheat_sheet_text.delete("1.0", tk.END)
                self.cheat_sheet_text.insert(tk.END, new_content)
                self.save_and_update_slides()
            else:
                messagebox.showinfo("Info", "No courses to delete.")
        else:
            messagebox.showinfo("Info", "No courses to delete.")

    def delete_appointment(self):
        content = self.cheat_sheet_text.get("1.0", tk.END)
        if "Appointments:" in content:
            parts = content.split("Appointments:")
            lines = parts[1].split('\n')
            if lines:
                lines.pop(0)  # Remove the first appointment
                parts[1] = '\n'.join(lines)
                new_content = parts[0] + "Appointments:" + parts[1]
                self.cheat_sheet_text.delete("1.0", tk.END)
                self.cheat_sheet_text.insert(tk.END, new_content)
                self.save_and_update_slides()
            else:
                messagebox.showinfo("Info", "No appointments to delete.")
        else:
            messagebox.showinfo("Info", "No appointments to delete.")

    def edit_course(self):
        content = self.cheat_sheet_text.get("1.0", tk.END)
        if "Upcoming Courses:" in content:
            parts = content.split("Upcoming Courses:")
            lines = parts[1].split('\n')
            if lines and lines[0]:
                course_info = lines[0].split(",")
                if len(course_info) == 5:
                    self.add_course()
                    self.cheat_sheet_text.delete("1.0", tk.END)
                    self.cheat_sheet_text.insert(tk.END, parts[0] + "Upcoming Courses:\n" + "\n".join(lines[1:]))
                else:
                    messagebox.showinfo("Info", "Invalid course format.")
            else:
                messagebox.showinfo("Info", "No courses to edit.")
        else:
            messagebox.showinfo("Info", "No courses to edit.")

    def edit_appointment(self):
        content = self.cheat_sheet_text.get("1.0", tk.END)
        if "Appointments:" in content:
            parts = content.split("Appointments:")
            lines = parts[1].split('\n')
            if lines and lines[0]:
                appointment_info = lines[0].split(",")
                if len(appointment_info) == 3:
                    self.add_appointment()
                    self.cheat_sheet_text.delete("1.0", tk.END)
                    self.cheat_sheet_text.insert(tk.END, parts[0] + "Appointments:\n" + "\n".join(lines[1:]))
                else:
                    messagebox.showinfo("Info", "Invalid appointment format.")
            else:
                messagebox.showinfo("Info", "No appointments to edit.")
        else:
            messagebox.showinfo("Info", "No appointments to edit.")

    def refresh_data(self):
        self.load_cheat_sheet()

    def show_help(self):
        messagebox.showinfo("Help", "Use the buttons on the left to add, edit, or delete courses and appointments.\n"
                                    "Save and Update Slides: Save changes and update the presentation.\n"
                                    "Add Course: Add a new course.\n"
                                    "Add Appointment: Add a new appointment.\n"
                                    "Delete Course: Delete the first course.\n"
                                    "Delete Appointment: Delete the first appointment.\n"
                                    "Edit Course: Edit the first course.\n"
                                    "Edit Appointment: Edit the first appointment.\n"
                                    "Refresh Data: Reload the cheat sheet data.\n"
                                    "Help: Show this help message.")

    def convert_to_dtg(self, date_text, time_text="00:00"):
        try:
            date_obj = datetime.datetime.strptime(date_text + " " + time_text, '%d-%m-%Y %H:%M')
            nz_timezone = pytz.timezone('Pacific/Auckland')
            date_obj = nz_timezone.localize(date_obj)

            dtg_date = date_obj.strftime('%d%H%MZ %b %y').upper()
            return dtg_date
        except ValueError:
            return None

    def setup_presentation(self):
        self.secondary_root.title("Presentation")

        self.image_label = tk.Label(self.secondary_root)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        generate_slides()
        self.slides = [os.path.join("slides", slide) for slide in os.listdir("slides") if slide.endswith('.png')]
        if not self.slides:
            self.image_label.config(text="No slides found in the 'slides' directory.")
            return

        self.current_slide = 0
        self.show_slide(self.current_slide)
        self.schedule_slide_switch()
        self.secondary_root.bind('<Configure>', self.resize_image)

    def show_slide(self, index):
        if 0 <= index < len(self.slides):
            self.current_image = Image.open(self.slides[index])
            self.resize_image()

    def resize_image(self, event=None):
        screen_width = self.secondary_root.winfo_width()
        screen_height = self.secondary_root.winfo_height()
        resized_image = self.current_image.resize((screen_width, screen_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def next_slide(self):
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
        else:
            self.current_slide = 0
        self.show_slide(self.current_slide)
        self.schedule_slide_switch()

    def schedule_slide_switch(self):
        self.secondary_root.after(10000, self.next_slide)
