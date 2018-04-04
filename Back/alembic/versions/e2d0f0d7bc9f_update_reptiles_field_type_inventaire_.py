"""update reptiles, field type_inventaire  values

Revision ID: e2d0f0d7bc9f
Revises: f4ed33963a7b
Create Date: 2018-03-30 11:49:23.021509

"""

# revision identifiers, used by Alembic.
revision = 'e2d0f0d7bc9f'
down_revision = 'f4ed33963a7b'

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
	SET "Options"= '["Crapaudrome/crapauduc","Nasse/piège aquatique","Observation fortuite","Plaque à reptiles","Point d''écoute nocturne","Recherche à vue","Troubleau"]'
    WHERE "TypeObj" = 3 AND "Name" = 'type_inventaire';
    '''
    op.execute(query)

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
