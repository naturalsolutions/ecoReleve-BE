"""add taxon as nom_latin in grid conf

Revision ID: 0a3422bb8b28
Revises: e126d4abea5f
Create Date: 2018-07-31 13:51:15.741396

"""

# revision identifiers, used by Alembic.
revision = '0a3422bb8b28'
down_revision = 'e126d4abea5f'

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
	"ID", "Module_ID", "TypeObj", "Name", "Label", "GridRender", "GridSize", "CellType", "GridOrder", "QueryName", "Options", "FilterOrder", "FilterSize", "IsSearchable", "FilterDefaultValue", "FilterRender", "FilterType", "FilterClass", "Status", "ColumnParams")
	VALUES (200,3,null,'nom_latin','Nom latin',1,'{"width": 120,"maxWidth": 350,"minWidth": 100}','string',50,'Forced',null,120,2,false,null,0,'TaxRefEditor',null,null,null)
    '''
    op.execute(query)

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
