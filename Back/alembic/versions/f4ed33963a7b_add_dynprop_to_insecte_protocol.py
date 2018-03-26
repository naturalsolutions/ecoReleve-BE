"""add dynprop to Insecte protocol

Revision ID: f4ed33963a7b
Revises: 695931a6ce47
Create Date: 2018-03-26 17:42:11.930990

"""

# revision identifiers, used by Alembic.
revision = 'f4ed33963a7b'
down_revision = '695931a6ce47'

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
    INSERT INTO "ProtocoleType_ObservationDynProp" ("FK_ObservationDynProp", "FK_ProtocoleType")
    SELECT "ID", (SELECT "ID" FROM "ProtocoleType" WHERE "Name" = 'Insectes') FROM "ObservationDynProp"
    WHERE "Name" IN ('taxref_id', 'nom_vernaculaire', 'type_milieu');
    '''
    op.execute(query)

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
