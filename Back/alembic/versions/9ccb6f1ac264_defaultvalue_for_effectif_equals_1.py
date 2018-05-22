"""defaultValue for effectif equals 1

Revision ID: 9ccb6f1ac264
Revises: d5b01e422773
Create Date: 2018-04-26 15:16:14.661775

"""

# revision identifiers, used by Alembic.
revision = '9ccb6f1ac264'
down_revision = 'd5b01e422773'

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
	SET "DefaultValue"= 1
    WHERE "Name" = 'effectif';
    '''
    op.execute(query)

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    query = '''
    UPDATE public."ModuleForms"
	SET "DefaultValue"= 0
    WHERE "Name" = 'effectif';
    '''
    op.execute(query)
