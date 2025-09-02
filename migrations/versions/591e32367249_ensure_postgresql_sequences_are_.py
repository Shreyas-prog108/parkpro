"""Ensure PostgreSQL sequences are properly configured

Revision ID: 591e32367249
Revises: 35ea3651fe94
Create Date: 2025-09-02 10:35:08.171217

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = '591e32367249'
down_revision = '35ea3651fe94'
branch_labels = None
depends_on = None


def upgrade():
    """
    Ensure all tables have proper PostgreSQL sequences for auto-increment primary keys.
    This migration is safe to run multiple times.
    """
    connection = op.get_bind()
    
    # Define tables that need sequences
    tables = ['user', 'parkinglot', 'spot', 'reservation', 'vehicle']
    
    for table in tables:
        sequence_name = f'{table}_id_seq'
        
        # Create sequence if it doesn't exist
        connection.execute(text(f'CREATE SEQUENCE IF NOT EXISTS {sequence_name};'))
        
        # Set column default to use sequence (handle 'user' as reserved word)
        if table == 'user':
            connection.execute(text(f'ALTER TABLE "{table}" ALTER COLUMN id SET DEFAULT nextval(\'{sequence_name}\');'))
            connection.execute(text(f'ALTER SEQUENCE {sequence_name} OWNED BY "{table}".id;'))
        else:
            connection.execute(text(f'ALTER TABLE {table} ALTER COLUMN id SET DEFAULT nextval(\'{sequence_name}\');'))
            connection.execute(text(f'ALTER SEQUENCE {sequence_name} OWNED BY {table}.id;'))
        
        # Set sequence value to be greater than current max ID
        if table == 'user':
            result = connection.execute(text(f'SELECT COALESCE(MAX(id), 0) FROM "{table}";'))
        else:
            result = connection.execute(text(f'SELECT COALESCE(MAX(id), 0) FROM {table};'))
        
        max_id = result.scalar() or 0
        if max_id > 0:
            connection.execute(text(f'SELECT setval(\'{sequence_name}\', {max_id + 1});'))


def downgrade():
    """
    Remove sequence defaults but keep sequences for safety.
    """
    connection = op.get_bind()
    
    # Define tables that have sequences
    tables = ['user', 'parkinglot', 'spot', 'reservation', 'vehicle']
    
    for table in tables:
        # Remove default from column (handle 'user' as reserved word)
        if table == 'user':
            connection.execute(text(f'ALTER TABLE "{table}" ALTER COLUMN id DROP DEFAULT;'))
        else:
            connection.execute(text(f'ALTER TABLE {table} ALTER COLUMN id DROP DEFAULT;'))
