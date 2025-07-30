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
│   └── ...
├── instance/
│   └── parking_details.db # SQLite database
└── venv/                 # Virtual environment
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

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vehicle-parking-app-v1
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-wtf wtforms
   ```

4. **Initialize the database**
   The database will be automatically created when you first run the application.

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your web browser and navigate to `http://localhost:5000`

## 👤 Default Admin Account

The application automatically creates a default admin account on first run:

- **Email**: `23f3001837@ds.study.iitm.ac.in`
- **Password**: `23f3001837_iitm`
- **Role**: Admin

> **Security Note**: Please change the default admin credentials in production!

## 🚦 Usage

### For Users

1. **Registration**: Create a new account with personal details
2. **Login**: Access your dashboard using email and password
3. **Add Vehicles**: Register your vehicles in the system
4. **Find Parking**: Browse available parking lots
5. **Book Spots**: Reserve parking spots for your vehicles
6. **Manage Reservations**: View and manage your bookings

### For Administrators

1. **Admin Dashboard**: Overview of all lots, spots, and users
2. **Create Parking Lots**: Add new parking locations with pricing
3. **Manage Spots**: Monitor spot availability and status
4. **User Management**: View registered users and their activities
5. **Analytics**: Access parking summaries and reports

## 🔧 Configuration

Key configuration options in `config.py`:

- **SECRET_KEY**: Flask session security key
- **SQLALCHEMY_DATABASE_URI**: Database connection string
- **Database Location**: `instance/parking_details.db` (as per memory: database should be located under the instance folder)

## 🛡️ Security Features

- **CSRF Protection**: All forms include CSRF tokens
- **Session Management**: Secure user sessions with Flask-Login
- **Role-based Access**: Separate admin and user access levels
- **Input Validation**: Form validation using WTForms

## 📱 API Endpoints

The application includes API endpoints for both admin and user operations:

- **Admin API**: Located in `api/admin_api.py`
- **User API**: Located in `api/user_api.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Known Issues & Limitations

- Passwords are stored in plain text (should implement hashing)
- No email verification for registration
- Limited error handling for edge cases
- Basic frontend styling (could be enhanced)

## 🔮 Future Enhancements

- [ ] Password hashing and security improvements
- [ ] Email verification system
- [ ] Payment integration
- [ ] Mobile responsive design
- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Export functionality for reports

## 📞 Support

For support, issues, or feature requests, please open an issue in the repository.

---

**ParkPro** - Making parking management simple and efficient! 🚗