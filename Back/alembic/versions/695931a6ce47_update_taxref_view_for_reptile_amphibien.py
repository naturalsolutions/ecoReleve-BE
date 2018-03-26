"""update TaxRef view for Reptile_amphibien

Revision ID: 695931a6ce47
Revises: 6d8232004c72
Create Date: 2018-03-26 12:24:18.748183

"""

# revision identifiers, used by Alembic.
revision = '695931a6ce47'
down_revision = '6d8232004c72'

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
    -- View: public.reptil_view
    -- DROP VIEW public.reptil_view;

    CREATE OR REPLACE VIEW public.reptil_view AS
    SELECT DISTINCT "TAXREF"."CD_NOM" AS taxref_id,
        "TAXREF"."NOM_VALIDE" AS latin,
        "TAXREF"."NOM_VERN" AS vernaculaire,
        "TAXREF"."RANG" AS rang
    FROM "TAXREF"
    WHERE "TAXREF"."GROUP2_INPN"::text IN ('Reptiles'::text, 'Amphibiens'::text ) AND "TAXREF"."FR"::text = 'P'::text AND "TAXREF"."CD_NOM" = "TAXREF"."CD_REF" AND ("TAXREF"."RANG"::text = ANY (ARRAY['ES'::character varying::text, 'GN'::character varying::text]));

    ALTER TABLE public.reptil_view
        OWNER TO postgres;
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
