import os
import datetime
import pytz
from PIL import Image, ImageDraw, ImageFont
import textwrap

def generate_slides():
    with open("slides/cheat_sheet.txt", "r") as file:
        lines = file.readlines()

    upcoming_courses_block = []
    appointments_block = []
    in_courses_section = False
    in_appointments_section = False

    for line in lines:
        if "Upcoming Courses:" in line:
            in_courses_section = True
            in_appointments_section = False
            continue
        elif "Appointments:" in line:
            in_courses_section = False
            in_appointments_section = True
            continue

        if in_courses_section:
            upcoming_courses_block.append(line.strip())
        elif in_appointments_section:
            appointments_block.append(line.strip())

    # Remove outdated appointments
    valid_appointments = []
    for appointment in appointments_block:
        parts = appointment.split(",")
        if len(parts) == 3:
            dtg_str = parts[2]
            try:
                dtg_date = datetime.datetime.strptime(dtg_str, '%d%H%MZ %b %y').replace(tzinfo=pytz.UTC)
                if dtg_date > (datetime.datetime.now(pytz.timezone('Pacific/Auckland')) - datetime.timedelta(days=1)).astimezone(pytz.UTC):
                    valid_appointments.append(appointment)
            except ValueError:
                continue
    appointments_block = valid_appointments

    # Sort appointments by date (latest first)
    appointments_block.sort(key=lambda x: datetime.datetime.strptime(x.split(",")[2], '%d%H%MZ %b %y').replace(tzinfo=pytz.UTC), reverse=True)

    slide_width = 1920
    slide_height = 1080

    # Generate slide for "Upcoming Courses"
    if upcoming_courses_block:
        image = Image.new("RGB", (slide_width, slide_height), "#f0f0f0")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 32)
        bold_font = ImageFont.truetype("arialbd.ttf", 32)
        y_text = 50
        headers = ["Course Name", "Start Date", "End Date", "People", "Details"]
        x_positions = [50, 300, 550, 800, 1050]

        # Draw headers
        for i, header in enumerate(headers):
            draw.text((x_positions[i], y_text), header, font=bold_font, fill="gray")
        y_text += 50  # Move down for rows

        for line in upcoming_courses_block:
            data = line.split(",", 4)  # Split into 5 parts (allowing commas in the last part)
            max_lines = 1
            for i, text in enumerate(data):
                if i < len(x_positions):  # Ensure there's no index error
                    wrap_width = 15 if i < 4 else 20  # Adjust wrap width for "Details" column
                    wrapped_text = textwrap.fill(text, width=wrap_width)
                    draw.text((x_positions[i], y_text), wrapped_text, font=font, fill="black")
                    lines = wrapped_text.count('\n') + 1
                    if lines > max_lines:
                        max_lines = lines
            y_text += max_lines * 50  # Adjust spacing between rows based on the tallest entry
        image.save("slides/slide1.png")

    # Generate slides for "Appointments"
    appointment_slides = []
    slide_content = []
    max_lines_per_slide = (slide_height - 100) // 50  # Approximate max number of lines per slide
    for line in appointments_block:
        slide_content.append(line)
        if len(slide_content) >= max_lines_per_slide:
            appointment_slides.append(slide_content)
            slide_content = []
    if slide_content:
        appointment_slides.append(slide_content)

    for i, slide_content in enumerate(appointment_slides):
        image = Image.new("RGB", (slide_width, slide_height), "#f0f0f0")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 32)
        bold_font = ImageFont.truetype("arialbd.ttf", 32)
        y_text = 50
        headers = ["Name", "Type of Appointment", "Date"]
        x_positions = [50, 400, 750]

        # Draw headers
        for j, header in enumerate(headers):
            draw.text((x_positions[j], y_text), header, font=bold_font, fill="gray")
        y_text += 50  # Move down for rows

        # Draw rows
        for line in slide_content:
            data = line.split(",", 3)  # Split into 4 parts (allowing commas in the last part)
            max_lines = 1
            for j, text in enumerate(data):
                if j < len(x_positions):  # Ensure there's no index error
                    wrap_width = 15 if j < 2 else 20  # Adjust wrap width for "Date" column
                    wrapped_text = textwrap.fill(text, width=wrap_width)
                    draw.text((x_positions[j], y_text), wrapped_text, font=font, fill="black")
                    lines = wrapped_text.count('\n') + 1
                    if lines > max_lines:
                        max_lines = lines
            y_text += max_lines * 50  # Adjust spacing between rows based on the tallest entry
        image.save(f"slides/slide2_{i}.png")
