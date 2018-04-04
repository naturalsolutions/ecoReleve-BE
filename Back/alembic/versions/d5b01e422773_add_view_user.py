"""add view user

Revision ID: d5b01e422773
Revises: e2d0f0d7bc9f
Create Date: 2018-04-04 17:12:01.537751

"""

# revision identifiers, used by Alembic.
revision = 'd5b01e422773'
down_revision = 'e2d0f0d7bc9f'

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
    
    query = '''
    CREATE OR REPLACE VIEW public."User" AS
    SELECT t."ID",
    t."Lastname",
    t."Firstname",
    t."CreationDate",
    t."Login",
    t."Language"
   FROM dblink('dbname=portal'::text, 'SELECT "TUse_PK_ID", "TUse_LastName", "TUse_FirstName", "TUse_CreationDate", "TUse_Login", "TUse_Language"
	FROM public."TUsers"'::text) t("ID" integer,
                                    "Lastname" character varying,
                                    "Firstname" character varying,
                                    "CreationDate" date ,
                                    "Login" character varying,
                                    "Language" character varying);

    '''
    op.execute(query)

def schema_downgrades():
    """schema downgrade migrations go here."""
    pass

def data_upgrades():
    """Add any optional data upgrade migrations here!"""
    pass

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
