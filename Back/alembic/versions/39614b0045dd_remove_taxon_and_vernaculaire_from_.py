"""remove taxon and vernaculaire from moduleGrids

Revision ID: 39614b0045dd
Revises: 376007ba4cd6
Create Date: 2020-03-30 23:52:16.355988

"""

# revision identifiers, used by Alembic.
revision = '39614b0045dd'
down_revision = '376007ba4cd6'

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
    query='''
    DELETE FROM public."ModuleGrids"
    WHERE
    "Module_ID" = 3
    AND
    "Name" = 'nom_vernaculaire';

    DELETE FROM public."ModuleGrids"
    WHERE
    "Module_ID" = 3
    AND
    "Name" = 'nom_latin';
    '''
    """schema downgrade migrations go here."""
    op.execute(sa.text(query))

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
