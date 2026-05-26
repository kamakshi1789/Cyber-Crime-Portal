# Cyber Secure India
### National Awareness Portal & Cyber Crime Incident Reporting System

A Flask-powered web application built for citizen cyber safety, incident filing, and administrative investigation tracking.

---

## 🚀 How to Run the Project

### 1. Install Prerequisites
Make sure you have **Python 3** installed on your system. Install the required libraries (Flask) using pip:
```bash
pip install -r requirements.txt
```
*If `requirements.txt` is empty or not installed, you can manually install the dependency:*
```bash
pip install Flask
```

### 2. Start the Server
Run the Flask main application file:
```bash
python app.py
```
This will start the local development server at `http://127.0.0.1:5000/`. Keep this terminal window open while using the application.

---

## 🎯 How to Open the Site & Slides

*   **Main Application**: Open your browser and go to **`http://127.0.0.1:5000/`**
*   **Interactive Presentation Slides (College Demo)**: Go to **`http://127.0.0.1:5000/presentation`**
    *   *Note:* This URL displays your university slides inside the web browser using DOM transitions and vector graphics.
    *   *Controls:* Use **Right/Left arrow keys**, the **Spacebar**, or the **Prev/Next buttons** on the screen to switch slides during your presentation.

---

## 📁 Directory Structure & File Usages

*   **`app.py`**: The core controller backend. Configures Flask routing, handles request session authorization (Citizen & Admin logins), database actions, and secures attachment file uploads.
*   **`database.db`**: The SQLite relational database storing tables for `users`, `complaints`, `admins`, and `contacts`.
*   **`requirements.txt`**: Standard file containing project library dependencies.
*   **`static/`**: Holds front-end styling and scripts.
    *   `css/style.css`: Clean, classic minimalist theme stylesheet styling navigation columns, alert ticks, and auth forms.
    *   `js/script.js`: Handles animation reveals on scrolling, stats dynamic counter ticker, and dashboard search filtering.
*   **`templates/`**: Directory containing HTML page components.
    *   `base.html`: Common frame containing navigation sidebars and dial helper links.
    *   `index.html`: Landing dashboard showing incident numbers and interactive tiles.
    *   `presentation.html`: The interactive HTML DOM slide presentation covering all 15 points.
    *   `login.html` / `register.html` / `admin_login.html`: Credential panels with centered container grids.
    *   `complaint.html` / `track.html`: Form interface to submit incident logs/evidence files, and search trackers.
    *   `admin_dashboard.html`: Master console for admins to audit and update progress categories.
    *   `sop.html` / `news.html` / `awareness.html` / `about.html` / `contact.html`: Information centers for digital hygiene SOP guidelines.
*   **`uploads/`**: Secure folder containing images or document evidence attachments uploaded during incident filings.
