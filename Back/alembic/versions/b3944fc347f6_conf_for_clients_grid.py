"""conf for clients grid

Revision ID: b3944fc347f6
Revises: 0c64dac54a42
Create Date: 2018-08-29 16:10:46.171659

"""

# revision identifiers, used by Alembic.
revision = 'b3944fc347f6'
down_revision = '0c64dac54a42'

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
    query ='''
    INSERT INTO public."ModuleGrids"(
	"ID","Module_ID", "TypeObj", "Name", "Label", "GridRender", "GridSize", "CellType", "GridOrder", "QueryName", "Options", "FilterOrder", "FilterSize", "IsSearchable", "FilterDefaultValue", "FilterRender", "FilterType", "FilterClass", "Status", "ColumnParams")
	VALUES 
	(200,23,NULL,'ID','ID',2,'{"width": 120,"maxWidth": 350,"minWidth": 100}','integer',1,NULL,NULL,10,2,true,NULL,4,'Text',NULL,NULL,'{"pinned" : "left" }'),
	(201,23,NULL,'Name','Nom',2,'{"width": 120,"maxWidth": 350,"minWidth": 100}','string',2,NULL,'{"source": "autocomplete/clients/Name", "minLength":3}',10,2,true,NULL,4,'AutocompleteEditor',NULL,NULL,NULL),
	(202,23,NULL,'description','Description',2,'{"width": 120,"maxWidth": 750,"minWidth": 100}','string',3,NULL,'{"source": "autocomplete/clients/description", "minLength":3}',10,2,true,NULL,4,'AutocompleteEditor',NULL,NULL,NULL);
    '''
    op.execute(query)

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
