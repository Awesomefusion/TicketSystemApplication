# Secure Ticket Management System

## Description
A simple, role-based ticketing application built with Python and Flask. Users can register, log in and manage support tickets, while administrators oversee assignments and maintain system integrity. The code is containerised with Docker and delivered via a CI/CD pipeline using GitHub Actions.

## Features
- User registration, login and logout
- Role-based access control (admin vs user)
- Create, view, update and delete tickets
- Comment on tickets
- Input validation and protection against common OWASP Top 10 vulnerabilities

## Technology Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Database:** SQLite
- **Containerisation:** Docker
- **CI/CD:** GitHub Actions

## Requirements
- Python 3.10+
- Docker (for containerisation)
- Git

## Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/Awesomefusion/TicketSystemApplication.git
   cd TicketSystemApplication

## Create and activate a virtual environment

python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

## Running the App

run `python run.py`

Browse to http://127.0.0.1:5000/ to log in or register.

## Testing

Create and activate virtual environment

run `pytest`

## Docker

docker build -t ticket-system .

docker run --env-file .env -p 5000:5000 ticket-system

Docker Repo: https://hub.docker.com/r/realfusion/ticketsystemapplication

## Docker Repository

https://hub.docker.com/r/realfusion/ticketsystemapplication/tags
