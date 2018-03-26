"""sort grid by date

Revision ID: 6d8232004c72
Revises: 25f3f7906272
Create Date: 2018-03-26 12:04:43.898125

"""

# revision identifiers, used by Alembic.
revision = '6d8232004c72'
down_revision = '25f3f7906272'

from alembic import op
import sqlalchemy as sa


from alembic import context



def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_upgrades()

def downgrade():
    if context.get_x_argument(as_dictionary=True).get('data', None):
        data_downgrades()
    schema_downgrades()

def schema_upgrades():
    """schema upgrade migrations go here."""
    pass

def schema_downgrades():
    """schema downgrade migrations go here."""
    pass

def data_upgrades():
    """Add any optional data upgrade migrations here!"""

    op.execute('''
        UPDATE "ModuleGrids" SET "ColumnParams" = '{"sort": "desc"}'
        WHERE "Name" = 'StationDate'
    ''')

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    
    op.execute('''
        UPDATE "ModuleGrids" SET "ColumnParams" = NULL
        WHERE "Name" = 'StationDate'
    ''')
