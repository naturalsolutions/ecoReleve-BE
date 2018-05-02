"""field name no longer required for stations 

Revision ID: e126d4abea5f
Revises: b7cb05e5b1ce
Create Date: 2018-05-02 17:24:57.010068

"""

# revision identifiers, used by Alembic.
revision = 'e126d4abea5f'
down_revision = 'b7cb05e5b1ce'

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
    UPDATE "ModuleForms" SET "Required" = 0
    WHERE "Name" = 'Name' AND "Module_ID" = 2
    ''')

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    op.execute('''
    UPDATE "ModuleForms" SET "Required" = 1
    WHERE "Name" = 'Name' AND "Module_ID" = 2
    ''')
    pass
