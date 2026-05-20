# CPU Scheduler Simulator

A web-based **CPU Scheduling Simulator** built with Python and JavaScript, designed to visualize and compare CPU scheduling algorithms. This project is perfect for students, developers, or anyone learning Operating System concepts.

---

## Features

- Implements the following CPU scheduling algorithms:
  - **FCFS (First Come First Served)**
  - **SJF (Shortest Job First)**
  - **Priority Scheduling (Non-preemptive)**
  - **Round Robin (Preemptive)**
- Visualizes execution using **Gantt Charts**.
- Displays metrics such as:
  - Average Waiting Time
  - Average Turnaround Time
  - Total Time
  - CPU Utilization
- Compare all algorithms side by side for analysis.
- User-friendly interface to add, remove, and clear processes.

---

## How to Download and Run

1. **Download the project**
   - Click the **Code → Download ZIP** button on GitHub.
   - Extract the folder to your desired location.

2. **Open in VS Code**
   - Launch **Visual Studio Code**.
   - Open the project folder via `File → Open Folder`.

3. **Install dependencies**
   - Make sure you have **Python 3.x** installed.
   - Open a terminal in VS Code and run:
     ```bash
     pip install Flask
     ```

4. **Run the project**
   - In the terminal, run:
     ```bash
     python app.py
     ```
   - The Flask server will start, and your default browser should open automatically.
   - If it doesn’t open automatically, go to:
     ```
     http://127.0.0.1:5000
     ```

5. **Using the Simulator**
   - **Add processes**: Enter PID, Arrival Time, Burst Time, and Priority.
   - **Select algorithm**: Choose FCFS, SJF, Priority, or Round Robin.
   - **Run Scheduler**: Click **Run Scheduler** to see the Gantt chart, metrics, and process table.
   - **Compare All**: Optionally, compare all algorithms to see performance differences.

---

## Project Files

- `app.py` - Flask backend for API and server
- `scheduler.py` - CPU scheduling algorithms and metrics
- `compare_test.py` - Test script for the API
- `script.js` - Frontend JavaScript for interactivity
- `index.html` - Frontend HTML template
- `style.css` - Optional styling for the frontend
- `README.md` - Project documentation (this file)

---

## Credits

**Project Author:** Abdul Moeed, AI Engineer  
**Institute:** Pak Austria Fachhochschule Institute of Applied Sciences  
**Supervisor:** Ms. Hamna Iqbal  

This project is designed for academic purposes and practical learning in Operating Systems.
