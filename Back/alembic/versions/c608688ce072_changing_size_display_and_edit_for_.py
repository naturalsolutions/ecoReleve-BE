"""changing size display and edit for checkbox

Revision ID: c608688ce072
Revises: 0a3422bb8b28
Create Date: 2018-08-29 10:19:46.839713

"""

# revision identifiers, used by Alembic.
revision = 'c608688ce072'
down_revision = '0a3422bb8b28'

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
    query = '''
    UPDATE public."ModuleForms"
    SET
    "FieldSizeEdit"=1,
    "FieldSizeDisplay"=1
    WHERE "Name" = 'estimated';
    '''
    op.execute(query)

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    query = '''
    UPDATE public."ModuleForms"
    SET
    "FieldSizeEdit"=3,
    "FieldSizeDisplay"=3
    WHERE "Name" = 'estimated';
    '''
    op.execute(query)

