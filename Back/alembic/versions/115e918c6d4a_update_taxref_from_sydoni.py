"""update taxref from sydoni

Revision ID: 115e918c6d4a
Revises: b3944fc347f6
Create Date: 2018-10-08 11:39:19.713232

"""

# revision identifiers, used by Alembic.
revision = '115e918c6d4a'
down_revision = 'b3944fc347f6'

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
    query ='''
    ------------------------------update insectes----------------------
    UPDATE public."TAXREF" SET "NOM_VERN" ='Aeschne subarctique' WHERE "CD_NOM" = 65432;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Topana cincticornis' WHERE "CD_NOM" = 65507;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Grillon manchois' WHERE "CD_NOM" = 65962;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Criquet hérisson, Criquet des Grands-Plans' WHERE "CD_NOM" = 66050;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Truxale méditerranéenne, Truxale occitane' WHERE "CD_NOM" = 66057;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Arcyptère languedocienne' WHERE "CD_NOM" = 66071;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Criquet de Jago' WHERE "CD_NOM" = 66082;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Oedipode rougeâtre' WHERE "CD_NOM" = 66206;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Criquet pèlerin' WHERE "CD_NOM" = 66229;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Miramelle des moraines' WHERE "CD_NOM" = 66235;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Miramelle des frimas' WHERE "CD_NOM" = 66239;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Criquet glauque' WHERE "CD_NOM" = 240287;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Argus de l''Hélianthème (L''), Argus marron (L'')' WHERE "CD_NOM" = 392262;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Criquet du Canigou' WHERE "CD_NOM" = 407264;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Criquet du Sampeyre' WHERE "CD_NOM" = 426091;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Éphippigère gasconne' WHERE "CD_NOM" = 432578;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Decticelle bariolée, Dectique brévipenne' WHERE "CD_NOM" = 593263;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Brachythémis à bandes brunes' WHERE "CD_NOM" = 814129;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Piéride de la roquette, Marbré oriental' WHERE "CD_NOM" = 833149;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Petit Agreste, Mercure' WHERE "CD_NOM" = 833422;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Mélitée catalane' WHERE "CD_NOM" = 833768;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Miramelle ligure' WHERE "CD_NOM" = 837204;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Mélitée sicilienne (La), Mélitée égéenne (La)' WHERE "CD_NOM" = 837241;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Selysiothémis noir' WHERE "CD_NOM" = 884487;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Trithémis à ailes ambrées' WHERE "CD_NOM" = 884489;

    ------------------------------update mamifere-------------------------------

    UPDATE public."TAXREF" SET "NOM_VERN" ='Souslik rouge' WHERE "CD_NOM" = 61197;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Rat brun, Rat gris, Surmulot' WHERE "CD_NOM" = 61585;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Lemming arctique, Lemming a collier, Lemming variable' WHERE "CD_NOM" = 199737;

    ------------------------------update oiseaux-------------------------------

    UPDATE public."TAXREF" SET "NOM_VERN" ='Pie-grièche isabelle' WHERE "CD_NOM" = 459630;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Hirondelle paludicole' WHERE "CD_NOM" = 534702;
    UPDATE public."TAXREF" SET "NOM_VERN" ='Ammomane élégante' WHERE "CD_NOM" = 886215;


    ----------------------------update reptiles et amphibiens----------------------------------------------

    UPDATE public."TAXREF" SET "NOM_VERN" ='Péloméduse roussâtre' WHERE "CD_NOM" = 844636;
    '''
    op.execute(sa.text(query))

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
