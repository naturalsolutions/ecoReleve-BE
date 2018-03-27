"""modify grid conf on station and clean depricated

Revision ID: d344da58480f
Revises: None
Create Date: 2018-03-26 11:17:31.995523

"""

# revision identifiers, used by Alembic.
revision = 'd344da58480f'
down_revision = None

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
            DELETE FROM "ModuleGrids"
            WHERE "Module_ID" IN (SELECT "ID" FROM "FrontModules" WHERE "Name" NOT IN ('ObservationForm'
                                                                ,'StationForm',
                                                                'StationGrid',
                                                                'ImportFileForm',
                                                                'ProjectForm',
                                                                'ProjectGrid',
                                                                'ClientForm',
                                                                'ClientGrid'));
            
            DELETE FROM "ModuleForms"
            WHERE "Module_ID" IN (SELECT "ID" FROM "FrontModules" WHERE "Name" NOT IN ('ObservationForm'
                                                                ,'StationForm',
                                                                'StationGrid',
                                                                'ImportFileForm',
                                                                'ProjectForm',
                                                                'ProjectGrid',
                                                                'ClientForm',
                                                                'ClientGrid'));

            DELETE FROM "FrontModules" WHERE "Name" NOT IN ('ObservationForm'
                                                                ,'StationForm',
                                                                'StationGrid',
                                                                'ImportFileForm',
                                                                'ProjectForm',
                                                                'ProjectGrid',
                                                                'ClientForm',
                                                                'ClientGrid');

            DELETE FROM "ModuleGrids" WHERE "Module_ID" = (SELECT "ID" FROM "FrontModules" WHERE "Name" = 'StationGrid') 
            AND "Name" NOT IN ('ID','StationDate','Name', 'LAT','LON', 'FK_ProtocoleType');

            UPDATE "ModuleGrids" SET "Options" = 'SELECT "ID" as val, "Label" as label FROM "ProtocoleType" order by "Label" ASC'
            WHERE "Name" = 'FK_ProtocoleType';
    '''
    op.execute(query)
    pass

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
