# Location and OTP-Based Authentication System

An authentication system that enhances security by verifying a user's location and sending a One-Time Password (OTP) for access.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Database Management](#database-management)
- [Dependencies](#dependencies)
- [License](#license)

## Overview

This project implements a two-factor authentication system that combines geographic location verification with OTPs. Users attempting to access the system are authenticated based on their physical location and a time-sensitive OTP sent to their registered contact method.

## Features

- **Location Verification:** Ensures that login attempts originate from authorized geographic locations.
- **OTP Authentication:** Sends a unique, time-sensitive OTP to users for enhanced security.
- **User Management:** Manages user data, including authentication credentials and location information.
- **Database Integration:** Utilizes SQLite for storing user information and authentication logs.

## Project Structure

```
location-and-otp-based-authentication/
├── instance/
│   └── ...
├── static/
│   └── ...
├── templates/
│   ├── index.html
│   ├── login.html
│   └── ...
├── TimeTable.xlsx
├── api_call/
│   ├── __init__.py
│   └── ...
├── app.py
├── create_db.py
├── keys.py
├── main.py
├── requirements.txt
└── student_data.xlsx
```

- `instance/`: Contains instance-specific files and configurations.
- `static/`: Stores static files such as CSS, JavaScript, and images.
- `templates/`: HTML templates for rendering web pages.
- `api_call/`: Module for handling API interactions.
- `app.py`: Main application script to run the Flask server.
- `create_db.py`: Script to initialize and manage the SQLite database.
- `keys.py`: Stores API keys and sensitive configurations.
- `main.py`: Entry point for the application.
- `requirements.txt`: Lists the Python dependencies required for the project.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ShreyashChilip/location-and-otp-based-authentication.git
   ```
2. **Navigate to the Project Directory:**
   ```bash
   cd location-and-otp-based-authentication
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **API Keys:** Populate the `keys.py` file with necessary API keys for services such as location verification and OTP delivery.
2. **Database Initialization:** Run the `create_db.py` script to set up the SQLite database.
   ```bash
   python create_db.py
   ```

## Usage

1. **Start the Application:** Run the Flask server using `app.py`.
   ```bash
   python app.py
   ```
2. **Access the Web Interface:** Open `http://localhost:5000` in a web browser.
3. **Login Process:**
   - Enter user credentials on the login page.
   - If the login attempt originates from an authorized location, an OTP is sent to the user's registered contact method.
   - Enter the received OTP to complete the authentication process.

## Database Management

- **User Data:** The `student_data.xlsx` file contains user information, which can be imported into the SQLite database.
- **Attendance Records:** The `TimeTable.xlsx` file manages attendance schedules and logs.

## Dependencies

- **Flask:** Web framework for Python.
- **SQLite:** Database for storing user and authentication data.
- **Requests:** Library for making HTTP requests.
- **Other Dependencies:** Listed in `requirements.txt`.

## License

This project is licensed under the [MIT License](LICENSE).
