"""add nbObs for ModuleGrids

Revision ID: 4fa574cc4c6b
Revises: 39614b0045dd
Create Date: 2020-03-31 00:10:51.707652

"""

# revision identifiers, used by Alembic.
revision = '4fa574cc4c6b'
down_revision = '39614b0045dd'

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
    INSERT INTO public."ModuleGrids"(
        "ID",
        "Module_ID",
        "Name",
        "Label",
        "GridRender",
        "GridSize",
        "CellType",
        "GridOrder",
        "QueryName",
        "FilterOrder",
        "FilterSize",
        "IsSearchable",
        "FilterRender",
        "FilterType"
        )
    VALUES (
        (select MAX("ID") + 1 FROM "ModuleGrids"),
        3,
        'nbObs',
        'Nb d’observations',
        2,
        '{"width": 120,"maxWidth": 350,"minWidth": 100}',
        'integer',
        40,
        'Forced',
        120,
        2,
        'false',
        0,
        4
        );
    '''
    op.execute(sa.text(query))

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
