"""add taxonfilter in modulegrid 

Revision ID: b7cb05e5b1ce
Revises: 9ccb6f1ac264
Create Date: 2018-05-02 16:47:25.535938

"""

# revision identifiers, used by Alembic.
revision = 'b7cb05e5b1ce'
down_revision = '9ccb6f1ac264'

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
    INSERT INTO public."ModuleGrids"
    ("ID","Module_ID","TypeObj","Name","Label","GridRender","GridSize","CellType","GridOrder","QueryName","Options","FilterOrder","FilterSize","IsSearchable","FilterDefaultValue","FilterRender","FilterType","FilterClass","Status","ColumnParams")
	VALUES
    (183,3,NULL,'nom_vernaculaire','Nom vernaculaire','1','{"width": 120,"maxWidth": 350,"minWidth": 100}','string',40,'Forced',NULL,120,2,false,NULL,0,'TaxRefEditor',NULL,NULL,NULL);
    '''
    op.execute(sa.text(query))

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    query ='''
    DELETE FROM public."ModuleGrids"
    WHERE "ID" = 183;
    '''
    op.execute(query)
