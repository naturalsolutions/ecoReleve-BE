"""add missing estimated checkbox and for each protocole add minimum checkbox

Revision ID: 0c64dac54a42
Revises: c608688ce072
Create Date: 2018-08-29 10:25:07.165858

"""

# revision identifiers, used by Alembic.
revision = '0c64dac54a42'
down_revision = 'c608688ce072'

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

    UPDATE public."ModuleForms"
    SET
    "FormOrder" = 30
    WHERE 
    "Name" = 'effectif' 
    AND 
    "TypeObj" = 6 ;

    UPDATE public."ModuleForms"
    SET
    "displayClass"='solo-input6',
    "EditClass"='solo-input6'
    WHERE 
    "Name" = 'stade' 
    AND 
    "TypeObj" = 6 ;

    INSERT INTO public."ModuleForms"
    ("Module_ID", "TypeObj", "Name", "Label", "Required", "FieldSizeEdit", "FieldSizeDisplay", "InputType", "editorClass", "displayClass", "EditClass", "FormRender", "FormOrder", "Legend", "Options", "Validators", "DefaultValue", "Rules")
    VALUES 
    (1,1,'minimum','Minimum',0,1,1,'Checkbox','form-control',NULL,NULL,7,6,'Obligatoire',NULL,NULL,'0',NULL),
    (1,3,'minimum','Minimum',0,1,1,'Checkbox','form-control',NULL,NULL,7,6,'Obligatoire',NULL,NULL,'0',NULL),
    (1,4,'minimum','Minimum',0,1,1,'Checkbox','form-control',NULL,NULL,7,6,'Obligatoire',NULL,NULL,'0',NULL),
    (1,5,'minimum','Minimum',0,1,1,'Checkbox','form-control',NULL,NULL,7,6,'Obligatoire',NULL,NULL,'0',NULL),
    (1,6,'estimated','Estimé',0,1,1,'Checkbox','form-control',NULL,NULL,7,31,'Facultatif',NULL,NULL,'0',NULL),
    (1,6,'minimum','Minimum',0,1,1,'Checkbox','form-control',NULL,NULL,7,32,'Facultatif',NULL,NULL,'0',NULL),
    (1,7,'estimated','Estimé',0,1,1,'Checkbox','form-control',NULL,NULL,7,6,'Obligatoire',NULL,NULL,'0',NULL),
    (1,7,'minimum','Minimum',0,1,1,'Checkbox','form-control',NULL,NULL,7,7,'Obligatoire',NULL,NULL,'0',NULL);


    INSERT INTO public."ObservationDynProp"("Name", "TypeProp")
	VALUES ( 'minimum', 'Integer');

    INSERT INTO public."ProtocoleType_ObservationDynProp"
    ("FK_ProtocoleType", "FK_ObservationDynProp")
    SELECT 
    distinct "ID" AS "FK_ProtocoleType",
    (SELECT "ID" FROM "ObservationDynProp" WHERE "Name" = 'minimum') AS "FK_ObservationDynProp"
    FROM "ProtocoleType"
    UNION
    SELECT 
    distinct
    "FK_ProtocoleType" AS "FK_ProtocoleType",
    (SELECT "ID" FROM "ObservationDynProp" WHERE "Name" = 'estimated') AS "FK_ObservationDynProp"
    FROM "ProtocoleType_ObservationDynProp"
    WHERE
    "FK_ProtocoleType" NOT IN (
    SELECT 
    "FK_ProtocoleType"
    FROM 
    public."ProtocoleType_ObservationDynProp"
    WHERE "FK_ObservationDynProp" = (SELECT "ID" FROM "ObservationDynProp" WHERE "Name" = 'estimated'));
    '''
    op.execute(query)

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
