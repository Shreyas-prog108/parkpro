# ParkPro - Vehicle Parking Management System

A comprehensive Flask-based web application for managing vehicle parking lots, reservations, and user accounts. This system provides separate dashboards for administrators and users with role-based access control.

## 🚀 Features

### For Users
- **User Registration & Authentication**: Secure login/logout with session management
- **Vehicle Management**: Add and manage multiple vehicles
- **Parking Lot Discovery**: Browse available parking lots with real-time spot availability
- **Spot Booking**: Reserve parking spots for specific vehicles
- **Reservation Management**: View active and past reservations
- **Cost Tracking**: Automatic calculation of parking costs based on duration

### For Administrators
- **Dashboard Overview**: Real-time statistics of all parking lots and users
- **Parking Lot Management**: Create, edit, and delete parking lots
- **Spot Management**: Monitor and manage individual parking spots
- **User Management**: View and manage registered users
- **Reservation Monitoring**: Track all active and completed reservations
- **Analytics**: View parking summaries and usage statistics

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Forms**: WTForms with CSRF protection
- **Frontend**: HTML templates with Jinja2
- **Styling**: Bootstrap (assumed from template structure)

## 📁 Project Structure

```
vehicle-parking-app-v1/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── forms.py              # WTForms definitions
├── admin_dashboard.py    # Admin blueprint and routes
├── user_dashboard.py     # User blueprint and routes
├── api/
│   ├── admin_api.py      # Admin API endpoints
│   └── user_api.py       # User API endpoints
├── templates/            # HTML templates
│   ├── admin_dash.html
│   ├── user_dash.html
│   ├── login.html
│   ├── register.html
│   ├── user_summary.html
│   ├── view_parking_status.html
│   ├── view_users.html
│   ├── parking_summary.html
│   ├── create_lot.html
│   ├── edit_lot.html
│
├── instance/
   └── parking_details.db # SQLite database
```

## 🗄️ Database Schema

The application uses the following main models:

- **User**: User accounts with role-based access (admin/user)
- **Vehicle**: User's registered vehicles
- **Parkinglot**: Parking lot locations with pricing
- **Spot**: Individual parking spots within lots
- **Reservation**: Booking records linking users, vehicles, and spots

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)



For support, issues, or feature requests, please open an issue in the repository.

---

**ParkPro** - Making parking management simple and efficient! 🚗
