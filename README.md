Schedule Display Manager
The Schedule Display Manager simplifies the process of managing and displaying course schedules and appointment times on a second screen. It's particularly useful in educational and training environments where keeping schedules up-to-date is essential.


Key Features
Course and Appointment Management:

Store and organize schedules in a spreadsheet.
Easily add, update, or remove entries to keep the display current.
Dynamic Display:

Present schedules in military Date-Time Group (DTG) format on a secondary screen.
Intuitive for military personnel.
Auto-Deletion:

Automatically remove entries 24 hours after their scheduled time.
Keeps the display uncluttered.
User-Friendly Interface:

GUI on a laptop stand allows users to seamlessly add new courses and appointments.
Real-time updates to the slideshow.
Use Cases
Military Training Facilities:
Ideal for displaying and managing training schedules in a military context.

Conference Rooms:
Useful in corporate or educational settings where schedules need to be frequently updated and displayed.

Getting Started
Prerequisites
Python 3.x
Required libraries as specified in requirements.txt
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/schedule-display-manager.git
Navigate to the project directory:

bash
Copy code
cd schedule-display-manager
Run the setup script:

bash
Copy code
setup_slides.bat
Usage
Run the application using the following command:

bash
Copy code
python main.py
Use the User Interface to add, update, or remove courses and appointments.

The display will automatically update in real-time.

Code Files
app.py: The main application file that initializes and runs the GUI and core functionalities.
generate_slides.py: Responsible for generating the slide content displayed on the secondary screen.
main.py: Entry point for running the Schedule Display Manager.
setup_slides.bat: A batch script that helps set up or initialize the slide generation process.
Version
Current Version: 0.1
License
This project is licensed under the MIT License - see the LICENSE file for details.
