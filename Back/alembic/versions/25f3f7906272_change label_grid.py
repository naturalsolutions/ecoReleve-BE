"""change label_grid

Revision ID: 25f3f7906272
Revises: d344da58480f
Create Date: 2018-03-26 11:20:42.601301

"""

# revision identifiers, used by Alembic.
revision = '25f3f7906272'
down_revision = 'd344da58480f'

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
     UPDATE "ModuleGrids" SET "Label" = 'Protocole'
     WHERE "Name" = 'FK_ProtocoleType'
    ''')


def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    op.execute('''
     UPDATE "ModuleGrids" SET "Label" = 'Protocole Type'
     WHERE "Name" = 'FK_ProtocoleType'
    ''')
