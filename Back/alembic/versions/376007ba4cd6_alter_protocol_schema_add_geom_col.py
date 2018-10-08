"""alter protocol schema add geom col

Revision ID: 376007ba4cd6
Revises: 115e918c6d4a
Create Date: 2018-10-08 11:50:58.067272

"""

# revision identifiers, used by Alembic.
revision = '376007ba4cd6'
down_revision = '115e918c6d4a'

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
    query ='''
        ALTER TABLE public."Observation"
        ADD COLUMN trace geometry(LineString);
        '''
    """schema upgrade migrations go here."""
    op.execute(query)

def schema_downgrades():
    """schema downgrade migrations go here."""
    pass

def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
