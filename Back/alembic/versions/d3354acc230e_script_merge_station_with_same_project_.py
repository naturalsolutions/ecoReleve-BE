"""script merge station with same project and same lat lon cascade merge observations

Revision ID: d3354acc230e
Revises: 4fa574cc4c6b
Create Date: 2020-03-31 00:55:34.894714

"""

# revision identifiers, used by Alembic.
revision = 'd3354acc230e'
down_revision = '4fa574cc4c6b'

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
    query='''
    BEGIN TRANSACTION;

    UPDATE "Observation"
    SET "FK_Station" = StationToKeep."ID"
    FROM (
        SELECT
        Sta."FK_Project" AS "FK_Project",
        MIN(Sta."ID") AS "ID",
        Sta."LAT" AS "LAT",
        Sta."LON" AS "LON"
        FROM "Station" AS Sta
        GROUP BY Sta."FK_Project",Sta."LAT",Sta."LON"
    ) AS StationToKeep
    JOIN "Station" AS StationToDel ON (
        StationToDel."LAT" = StationToKeep."LAT"
        AND
        StationToDel."LON" = StationToKeep."LON"
        AND
        StationToDel."FK_Project" = StationToKeep."FK_Project"
        AND
        StationToDel."ID" <> StationToKeep."ID"
    )
    WHERE
    "Observation"."FK_Station"  = StationToDel."ID";

    DELETE FROM "Station"
    WHERE "ID" IN (
    SELECT
    StationToDel."ID"
    FROM (
        SELECT
        Sta."FK_Project" AS "FK_Project",
        MIN(Sta."ID") AS "ID",
        Sta."LAT" AS "LAT",
        Sta."LON" AS "LON"
        FROM "Station" AS Sta
        GROUP BY Sta."FK_Project",Sta."LAT",Sta."LON"
    ) AS StationToKeep
    JOIN "Station" AS StationToDel ON (
        StationToDel."LAT" = StationToKeep."LAT"
        AND
        StationToDel."LON" = StationToKeep."LON"
        AND
        StationToDel."FK_Project" = StationToKeep."FK_Project"
        AND
        StationToDel."ID" <> StationToKeep."ID"
    )
    );

    COMMIT TRANSACTION ;
    '''
    op.execute(sa.text(query))

def data_downgrades():
    """Add any optional data downgrade migrations here!"""
    pass
