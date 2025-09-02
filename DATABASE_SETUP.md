# Database Setup for ParkPro

## PostgreSQL Auto-Increment Setup

This project uses Flask-Migrate to handle database migrations and automatic setup of PostgreSQL sequences for auto-increment primary keys.

### How It Works

1. **Migration System**: The project includes a special migration (`591e32367249`) that automatically sets up PostgreSQL sequences for all tables with auto-increment primary keys.

2. **Automatic Deployment**: The `start.sh` script runs `flask db upgrade` on startup, which ensures all migrations (including sequence setup) are applied automatically.

3. **Safe to Run Multiple Times**: The sequence setup migration is designed to be idempotent - it can be run multiple times safely without causing errors.

### Tables with Auto-Increment IDs

- `user` - User accounts
- `parkinglot` - Parking lot locations  
- `spot` - Individual parking spots
- `reservation` - Parking reservations
- `vehicle` - User vehicles

### For New Deployments

When deploying to a fresh environment:

1. The Docker container starts
2. `start.sh` runs `flask db upgrade`
3. All migrations are applied, including sequence setup
4. Users can register without any manual intervention

### For Development

If you're setting up a local development environment:

```bash
# Set up database
flask db upgrade

# Test user creation (should work automatically)
python -c "
from app import app, db
from models import User
with app.app_context():
    user = User(email='test@example.com', password='pass', name='Test', pincode=123456, address='Test Address')
    db.session.add(user)
    db.session.commit()
    print(f'Created user with ID: {user.id}')
"
```

### Troubleshooting

If you encounter sequence-related errors:

1. Check if the migration has been applied: `flask db current`
2. Run the upgrade manually: `flask db upgrade`
3. The system should automatically handle sequence conflicts

The auto-increment setup is fully automated and requires no manual intervention for user registration or any other record creation.
