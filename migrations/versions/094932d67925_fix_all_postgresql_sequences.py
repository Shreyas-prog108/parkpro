"""fix all postgresql sequences

Revision ID: 094932d67925
Revises: 591e32367249
Create Date: 2025-09-04 14:32:28.218505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '094932d67925'
down_revision = '591e32367249'
branch_labels = None
depends_on = None


def upgrade():
    """Fix all PostgreSQL sequences to start from the correct value"""
    # Get current connection
    connection = op.get_bind()
    
    # List of tables with auto-incrementing primary keys
    tables = ['user', 'vehicle', 'parkinglot', 'spot', 'reservation']
    
    for table_name in tables:
        try:
            # Get the maximum ID from the table
            result = connection.execute(sa.text(f'SELECT COALESCE(MAX(id), 0) FROM "{table_name}"'))
            max_id = result.scalar()
            
            # Set the sequence to start from max_id + 1
            sequence_name = f'{table_name}_id_seq'
            connection.execute(sa.text(f'SELECT setval(\'{sequence_name}\', {max_id + 1})'))
            
            print(f'Fixed sequence for {table_name}: set to {max_id + 1}')
        except Exception as e:
            print(f'Error fixing sequence for {table_name}: {e}')
            # Continue with other tables even if one fails


def downgrade():
    # No downgrade needed for sequence fixes
    pass
